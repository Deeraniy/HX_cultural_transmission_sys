from transformers import pipeline
import pandas as pd
import logging
from django.shortcuts import render, redirect,HttpResponse
import pymysql
import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET
# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 初始化情感分析模型
distilled_student_sentiment_classifier = pipeline(
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", 
    return_all_scores=True
)

def get_sentiment_label(text):
    """获取文本的情感标签和得分"""
    try:
        results = distilled_student_sentiment_classifier(text)[0]  # 获取分析结果
        # 找出得分最高的标签
        max_score_label = max(results, key=lambda x: x['score'])
        return max_score_label['label'], max_score_label['score']
    except Exception as e:
        logger.error(f"处理文本时出错: {text}. 错误信息: {str(e)}")
        return 'error', 0.0

def process_comments(comments_list):
    """处理评论列表并返回带标签的DataFrame"""
    results = []
    for comment in comments_list:
        label, score = get_sentiment_label(comment)
        results.append({
            'comment': comment,
            'sentiment': label,
            'confidence': score
        })
    return results

def sentiments_analyze(request):
    spot_name = request.GET.get('spot_name')
    conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                           db='hx_cultural_transmission_sys',charset='utf8')

    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    spot_id=cursor.execute("SELECT spot_id FROM scenicspot WHERE spot_name=%s",(spot_name))
    sql_query = "SELECT content FROM usercomment WHERE spot_id=%s"
    # 执行SQL，并返回收影响行数
    effect_row = cursor.execute(sql_query, (spot_id))
    comment_list =cursor.fetchall()
    # print(comment_list)
    comment_list = [comment['content'] for comment in comment_list]
    results=process_comments(comment_list)
    cursor.close()
    conn.close()
    # 处理结果
    return JsonResponse(results, safe=False)


def sentiments_all():
    """对所有评论进行情感分析并更新数据库"""
    try:
        # 建立数据库连接
        conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                             db='hx_cultural_transmission_sys', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        
        # 获取所有评论
        cursor.execute("SELECT id, content FROM usercomment")
        comments = cursor.fetchall()
        
        # 逐条处理评论
        for comment in comments:
            sentiment_label, confidence = get_sentiment_label(comment['content'])
            logging.info(f"评论ID: {comment['id']}, 情感标签: {sentiment_label}, 置信度: {confidence}")
            # 更新数据库
            update_sql = """
                UPDATE usercomment 
                SET sentiment = %s, sentiment_confidence = %s 
                WHERE id = %s
            """
            cursor.execute(update_sql, (sentiment_label, confidence, comment['id']))
            
        # 提交更改
        conn.commit()
        logger.info("所有评论的情感分析已完成并更新到数据库")
        
    except Exception as e:
        logger.error(f"情感分析过程中出错: {str(e)}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
    

def sentiment_month_analyze(sentiments):
    """
    计算每月的情感得分和主导情感
    sentiments: 包含 sentiment 和 confidence 的列表
    """
    # 计算加权得分：positive=1, neutral=0.5, negative=0
    score = 0
    total_comments = len(sentiments)
    
    for sent, conf in sentiments:
        if sent == 'positive':
            score += conf * 1
        elif sent == 'neutral':
            score += conf * 0.5
        elif sent == 'negative':
            score += conf * 0
    
    # 计算平均分
    avg_score = score / total_comments if total_comments > 0 else 0
    
    # 确定主导情感
    if avg_score > 0.7:
        dominant_sentiment = 'positive'
    elif avg_score < 0.3:
        dominant_sentiment = 'negative'
    else:
        dominant_sentiment = 'neutral'
        
    return avg_score, dominant_sentiment

def sentiments_result_total_count(request):
    """获取景点的情感分析占比统计"""
    try:
        spot_name = request.GET.get('spot_name', '').strip()
        if not spot_name:
            return JsonResponse({
                'status': 'error',
                'message': '景点名称不能为空'
            }, status=400)
            
        logger.info(f"正在查询景点: {spot_name}")
            
        # 数据库连接
        conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', 
                             passwd='kissme77', db='hx_cultural_transmission_sys', 
                             charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 首先获取景点ID
        spot_sql = "SELECT spot_id FROM scenicspot WHERE spot_name = %s"
        cursor.execute(spot_sql, (spot_name,))
        spot_result = cursor.fetchone()
        
        if not spot_result:
            return JsonResponse({
                'status': 'error',
                'message': f'未找到景点: {spot_name}'
            }, status=404)
            
        spot_id = spot_result['spot_id']
        
        # 查询各情感类型的评论数量和占比
        sentiment_sql = """
            SELECT 
                sentiment,
                COUNT(*) as count,
                COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() as percentage
            FROM usercomment 
            WHERE spot_id = %s AND sentiment IS NOT NULL
            GROUP BY sentiment
        """
        cursor.execute(sentiment_sql, (spot_id,))
        results = cursor.fetchall()
        
        # 初始化结果字典
        sentiment_stats = {
            'positive': 0,
            'neutral': 0,
            'negative': 0,
            'total_count': 0
        }
        
        # 处理查询结果
        for row in results:
            if row['sentiment'] in sentiment_stats:
                sentiment_stats[row['sentiment']] = round(row['percentage'], 2)
                sentiment_stats['total_count'] += row['count']

        return JsonResponse({
            'status': 'success',
            'data': {
                'positive_percentage': sentiment_stats['positive'],
                'neutral_percentage': sentiment_stats['neutral'],
                'negative_percentage': sentiment_stats['negative'],
                'total_comments': sentiment_stats['total_count']
            }
        })

    except Exception as e:
        logger.error(f"获取情感统计时出错: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@require_GET
def sentiments_result(request):
    """根据景点名称获取情感分析时间序列结果"""
    try:
        spot_name = request.GET.get('spot_name', '').strip()
        if not spot_name:
            return JsonResponse({
                'status': 'error',
                'message': '景点名称不能为空'
            }, status=400)
            
        logger.info(f"正在查询景点: {spot_name}")
            
        # 数据库连接
        conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', 
                             passwd='kissme77', db='hx_cultural_transmission_sys', 
                             charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        
        # 修正：使用正确的字段名 spot_name 而不是 name
        spot_sql = "SELECT spot_id FROM scenicspot WHERE spot_name = %s LIMIT 1"
        cursor.execute(spot_sql, (spot_name,))
        spot_result = cursor.fetchone()
        
        if not spot_result:
            return JsonResponse({
                'status': 'error',
                'message': f'未找到景点: {spot_name}'
            }, status=404)
            
        # 修正：使用正确的字段名 spot_id 而不是 id
        spot_id = spot_result['spot_id']  # 改用 'spot_id' 而不是 'id'
        logger.info(f"找到景点ID: {spot_id}")
        
        # 查询评论数据
        comment_sql = """
            SELECT 
                sentiment, 
                sentiment_confidence, 
                SUBSTRING_INDEX(LEFT(create_time, 7), '-', 1) as year,
                SUBSTRING_INDEX(LEFT(create_time, 7), '-', -1) as month
            FROM usercomment 
            WHERE spot_id = %s AND sentiment IS NOT NULL
            ORDER BY create_time
        """
        cursor.execute(comment_sql, (spot_id,))
        results = cursor.fetchall()
        # print(results)
        
        if not results:
            return JsonResponse({
                'status': 'success',
                'data': [],
                'spot_info': {
                    'name': spot_name,
                    'id': spot_id
                },
                'message': '该景点暂无评论数据'
            })
        
        # 按年月分组数据
        print(results)
        monthly_data = {}
        for row in results:
            date_key = f"{row['year']}-{row['month']}"
            if date_key not in monthly_data:
                monthly_data[date_key] = []
            
            if row['sentiment'] and row['sentiment_confidence']:
                monthly_data[date_key].append(
                    (row['sentiment'], float(row['sentiment_confidence']))
                )
        
        # 计算每月的情感分析结果
        analysis_results = []
        for year_month, sentiments in monthly_data.items():
            year, month = map(int, year_month.split('-'))
            # 直接使用元组列表
            sentiment_score, dominant_sentiment = sentiment_month_analyze(sentiments)
            
            analysis_results.append({
                'year': year,
                'month': month,
                'sentiment_score': round(sentiment_score, 3),
                'sentiment': dominant_sentiment,
                'comment_count': len(sentiments)
            })
        
        # 按时间排序
        analysis_results.sort(key=lambda x: (x['year'], x['month']))
        
        return JsonResponse({
            'status': 'success',
            'data': analysis_results,
            'spot_info': {
                'name': spot_name,
                'id': spot_id
            }
        })
        
    except Exception as e:
        logger.error(f"处理景点 {spot_name} 的情感分析时出错: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

from zhipuai import ZhipuAI
client = ZhipuAI(api_key="1af4f35363ea97ed269ee3099c04f7f3.3AGroi22UtegCtjf")  # 请替换为您的真实API密钥

def generate_report(request):
    """
    基于情感分析结果生成报告的API
    """
    try:
        # 获取景点名称
        spot_name = request.GET.get('spot_name', '').strip()
        if not spot_name:
            return JsonResponse({
                'status': 'error',
                'message': '景点名称不能为空'
            }, status=400)

        # 调用情感分析API获取数据
        sentiment_response = sentiments_result(request)
        sentiment_data = json.loads(sentiment_response.content)

        if sentiment_data['status'] != 'success':
            return JsonResponse({
                'status': 'error',
                'message': sentiment_data.get('message', '获取情感分析数据失败')
            }, status=400)

        data = sentiment_data['data']
        
        # 处理数据，计算每个月的统计信息
        monthly_stats = {}
        for entry in data:
            year = entry['year']
            month = entry['month']
            sentiment = entry['sentiment']
            sentiment_score = entry['sentiment_score']
            comment_count = entry['comment_count']
            
            key = (year, month)
            if key not in monthly_stats:
                monthly_stats[key] = {
                    'total_comments': 0,
                    'sentiment_counts': {'positive': 0, 'neutral': 0, 'negative': 0},
                    'sentiment_scores': {'positive': [], 'neutral': [], 'negative': []},
                }
            monthly_stats[key]['total_comments'] += comment_count
            monthly_stats[key]['sentiment_counts'][sentiment] += comment_count
            monthly_stats[key]['sentiment_scores'][sentiment].append(sentiment_score * comment_count)

        # 计算百分比和平均情感得分
        for key in monthly_stats:
            stats = monthly_stats[key]
            total_comments = stats['total_comments']
            for sentiment in ['positive', 'neutral', 'negative']:
                count = stats['sentiment_counts'][sentiment]
                percentage = (count / total_comments) * 100 if total_comments > 0 else 0
                total_score = sum(stats['sentiment_scores'][sentiment])
                avg_score = (total_score / count) if count > 0 else 0
                stats['sentiment_counts'][sentiment] = {'count': count, 'percentage': percentage}
                stats['sentiment_scores'][sentiment] = avg_score

        # 构建提示语
        prompt = f"我已经完成了{spot_name}景点的情感分析，分析结果如下：\n\n"
        for key in sorted(monthly_stats.keys()):
            year, month = key
            stats = monthly_stats[key]
            prompt += f"{year}年{month}月:\n"
            total_comments = stats['total_comments']
            prompt += f"- 总评论数：{total_comments}\n"
            for sentiment in ['positive', 'neutral', 'negative']:
                count_info = stats['sentiment_counts'][sentiment]
                avg_score = stats['sentiment_scores'][sentiment]
                sentiment_chinese = {'positive': '正面', 'neutral': '中性', 'negative': '负面'}[sentiment]
                if count_info['count'] > 0:
                    if count_info['percentage'] == 100:
                        prompt += f"  - {sentiment_chinese}评论占比居多\n"
                    else:
                        prompt += f"  - {sentiment_chinese}反馈：{count_info['count']}条，占比{count_info['percentage']:.2f}%\n"
                    prompt += f"    - 平均情感得分：{avg_score:.2f}\n"
            prompt += "\n"

        prompt += "请基于以上数据，帮助我生成一份情感分析报告，包括每个月的情感趋势和总体总结，使用幽默的语调。请不要包括改进建议。"

        # 调用 ZhipuAI 的聊天模型
        client = ZhipuAI(api_key="1af4f35363ea97ed269ee3099c04f7f3.3AGroi22UtegCtjf")
        response = client.chat.completions.create(
            model="chatglm_std",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        report = response.choices[0].message.content.strip()
        
        return JsonResponse({
            'status': 'success',
            'report': report,
            'spot_name': spot_name
        })

    except Exception as e:
        logger.error(f"生成报告时出错: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

# 使用示例
if __name__ == "__main__":
    # 示例评论列表
    comments = [
        "今天真是个坏天气,才怪",
        "I love this movie and i would watch it again and again!",
        "这个产品质量太差了",
        "Service was just okay"
    ]
    
    # 处理评论
    results_df = process_comments(comments)
    logger.info(f"处理完成，结果如下：\n{results_df}")
    
    sentiments_all()