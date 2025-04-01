import pymysql
import logging
import json
from django.http import JsonResponse
from transformers import pipeline
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="1af4f35363ea97ed269ee3099c04f7f3.3AGroi22UtegCtjf")

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 初始化情感分析模型
sentiment_classifier = pipeline(
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student",
    return_all_scores=True
)

def get_folk_sentiment_label(text):
    """获取民间评论的情感标签和得分"""
    try:
        results = sentiment_classifier(text)[0]
        max_score_label = max(results, key=lambda x: x['score'])
        return max_score_label['label'], max_score_label['score']
    except Exception as e:
        logger.error(f"处理民间评论文本时出错: {text}. 错误信息: {str(e)}")
        return 'error', 0.0

def process_user_comment_folk(comments_list):
    """处理民间评论列表并返回带标签的DataFrame"""
    results = []
    for comment in comments_list:
        label, score = get_folk_sentiment_label(comment)
        results.append({
            'comment': comment,
            'sentiment': label,
            'confidence': score
        })
    return results

def sentiments_all():
    """对所有民间评论进行情感分析并更新数据库"""
    try:
        conn = pymysql.connect(
            host='8.148.26.99',
            port=3306,
            user='root',
            passwd='song',
            db='hx_cultural_transmission_sys',
            charset='utf8',
            connect_timeout=10,
            read_timeout=30,
            write_timeout=30,
            autocommit=True
        )
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        cursor.execute("SELECT comment_id, comment_text FROM user_comment_folk WHERE sentiment IS NULL")
        comments = cursor.fetchall()

        processed_count = 0

        for comment in comments:
            try:
                sentiment_label, confidence = get_folk_sentiment_label(comment['comment_text'])
                logger.info(f"评论ID: {comment['comment_id']}, 情感标签: {sentiment_label}, 置信度: {confidence}")

                update_sql = """
                    UPDATE user_comment_folk 
                    SET sentiment = %s, sentiment_confidence = %s 
                    WHERE comment_id = %s
                """
                cursor.execute(update_sql, (sentiment_label, confidence, comment['comment_id']))
                processed_count += 1

                if processed_count % 10 == 0:
                    logger.info(f"已处理 {processed_count} 条评论")

            except pymysql.Error as e:
                logger.error(f"数据库操作出错 (评论ID: {comment['comment_id']}): {str(e)}")
                continue
            except Exception as e:
                logger.error(f"处理评论时出错 (评论ID: {comment['comment_id']}): {str(e)}")
                continue

        logger.info(f"所有民间评论的情感分析已完成，共处理 {processed_count} 条评论")

    except Exception as e:
        logger.error(f"情感分析过程中出错: {str(e)}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.open:
            conn.close()

def sentiments_analyze(request):
    """获取民间评论的情感分析"""
    folk_name = request.GET.get('name')
    try:
        conn = pymysql.connect(
            host='8.148.26.99',
            port=3306,
            user='root',
            passwd='song',
            db='hx_cultural_transmission_sys',
            charset='utf8'
        )
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        cursor.execute("SELECT folk_id FROM folk WHERE folk_name=%s", (folk_name,))
        folk_result = cursor.fetchone()

        if not folk_result:
            return JsonResponse({
                'status': 'error',
                'message': f'未找到民间: {folk_name}'
            }, status=404)

        sql_query = "SELECT comment_text FROM user_comment_folk WHERE folk_id=%s"
        cursor.execute(sql_query, (folk_result['folk_id'],))
        comment_list = cursor.fetchall()

        comment_list = [comment['comment_text'] for comment in comment_list]

        results = process_user_comment_folk(comment_list)

        cursor.close()
        conn.close()

        return JsonResponse(results, safe=False)

    except Exception as e:
        logger.error(f"处理民间评论情感分析时出错: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

def sentiment_month_analyze(sentiments):
    """
    计算每月的情感得分和主导情感
    sentiments: 包含 sentiment 和 confidence 的列表
    """
    score = 0
    total_comments = len(sentiments)

    for sent, conf in sentiments:
        if sent == 'positive':
            score += conf * 1
        elif sent == 'neutral':
            score += conf * 0.5
        elif sent == 'negative':
            score += conf * 0

    avg_score = score / total_comments if total_comments > 0 else 0

    if avg_score > 0.7:
        dominant_sentiment = 'positive'
    elif avg_score < 0.3:
        dominant_sentiment = 'negative'
    else:
        dominant_sentiment = 'neutral'

    return avg_score, dominant_sentiment

def sentiments_result_total_count(request):
    """获取非遗民俗的情感分析占比统计"""
    try:
        name = request.GET.get('name', '').strip()
        if not name:
            return JsonResponse({
                'status': 'error',
                'message': '非遗民俗名称不能为空'
            }, status=400)

        logger.info(f"正在查询非遗民俗: {name}")

        # 数据库连接
        conn = pymysql.connect(host='8.148.26.99', port=3306, user='root',
                             passwd='song', db='hx_cultural_transmission_sys',
                             charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 首先获取非遗民俗ID
        folk_sql = "SELECT folk_id FROM folk WHERE folk_name = %s"
        cursor.execute(folk_sql, (name,))
        folk_result = cursor.fetchone()

        if not folk_result:
            return JsonResponse({
                'status': 'error',
                'message': f'未找到非遗民俗: {name}'
            }, status=404)

        folk_id = folk_result['folk_id']

        # 查询各情感类型的评论数量和占比
        sentiment_sql = """
            SELECT 
                sentiment,
                COUNT(*) as count,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) 
                    FROM user_comment_folk 
                    WHERE folk_id = %s AND sentiment IS NOT NULL AND sentiment != ''
                ), 2) as percentage
            FROM user_comment_folk 
            WHERE folk_id = %s AND sentiment IS NOT NULL AND sentiment != ''
            GROUP BY sentiment
        """
        cursor.execute(sentiment_sql, (folk_id, folk_id))
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

def sentiments_result(request):
    """根据民间作品名称获取情感分析时间序列结果"""
    try:
        folk_name = request.GET.get('name', '').strip()
        if not folk_name:
            return JsonResponse({
                'status': 'error',
                'message': '民间名称不能为空'
            }, status=400)

        logger.info(f"正在查询民间: {folk_name}")

        conn = pymysql.connect(host='8.148.26.99', port=3306, user='root',
                             passwd='song', db='hx_cultural_transmission_sys',
                             charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        cursor.execute("SELECT folk_id FROM folk WHERE folk_name = %s LIMIT 1", (folk_name,))
        folk_result = cursor.fetchone()

        if not folk_result:
            return JsonResponse({
                'status': 'error',
                'message': f'未找到民间: {folk_name}'
            }, status=404)

        folk_id = folk_result['folk_id']
        logger.info(f"找到民间ID: {folk_id}")

        comment_sql = """
            SELECT 
                sentiment, 
                sentiment_confidence, 
                SUBSTRING_INDEX(LEFT(comment_time, 7), '-', 1) as year,
                SUBSTRING_INDEX(LEFT(comment_time, 7), '-', -1) as month
            FROM user_comment_folk 
            WHERE folk_id = %s AND sentiment IS NOT NULL
            ORDER BY comment_time
        """
        cursor.execute(comment_sql, (folk_id,))
        results = cursor.fetchall()

        if not results:
            return JsonResponse({
                'status': 'success',
                'data': [],
                'folk_info': {
                    'name': folk_name,
                    'id': folk_id
                },
                'message': '该民间暂无评论数据'
            })

        # 按年月分组数据
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
            sentiment_score, dominant_sentiment = sentiment_month_analyze(sentiments)

            analysis_results.append({
                'year': year,
                'month': month,
                'sentiment_score': round(sentiment_score, 3),
                'sentiment': dominant_sentiment,
                'comment_count': len(sentiments)
            })

        analysis_results.sort(key=lambda x: (x['year'], x['month']))

        return JsonResponse({
            'status': 'success',
            'data': analysis_results,
            'folk_info': {
                'name': folk_name,
                'id': folk_id
            }
        })

    except Exception as e:
        logger.error(f"处理民间 {folk_name} 的情感分析时出错: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def generate_report(request):
    """生成AI分析报告"""
    try:
        name = request.GET.get('name', '').strip()
        if not name:
            return JsonResponse({
                'status': 'error',
                'message': '非遗民俗名称不能为空'
            }, status=400)

        # 获取情感分析结果
        sentiment_response = sentiments_result(request)
        sentiment_data = sentiment_response.content if isinstance(sentiment_response.content, dict) else json.loads(sentiment_response.content.decode('utf-8'))

        if sentiment_data['status'] != 'success':
            return JsonResponse({
                'status': 'error',
                'message': sentiment_data.get('message', '获取情感分析数据失败')
            }, status=400)

        data = sentiment_data.get('data', [])

        # 处理数据，计算每个月的统计信息
        monthly_stats = {}
        timeline_data = []  # 新增：用于存储时间轴数据
        for entry in data:
            year = entry['year']
            month = entry['month']
            sentiment = entry['sentiment']
            sentiment_score = entry['sentiment_score']
            comment_count = entry['comment_count']

            # 添加到时间轴数据
            timeline_data.append({
                'date': f'{year}-{month:02d}',
                'sentiment': sentiment,
                'score': sentiment_score,
                'count': comment_count
            })

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
        prompt = "我已经完成了情感分析，分析结果如下：\n\n"
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

        # 修改提示语，要求使用幽默的语调，并不包括改进建议
        prompt += (
            "请基于以上数据，帮助我生成一份情感分析报告，包括每个月的情感趋势和总体总结，"
            "使用幽默的语调,并在报告中多使用emoji和颜文字请不要包括改进建议。"
            "请在总结部分详细分析整体情感趋势，深入探讨可能的原因和影响，多写一些内容。"
        )

        # 调用 ZhipuAI 的聊天模型
        response = client.chat.completions.create(
            model="chatglm_lite",
            messages=[{"role": "user", "content": prompt}]
        )

        report = response.choices[0].message.content.strip()

        # 按日期排序时间轴数据
        timeline_data.sort(key=lambda x: x['date'])

        return JsonResponse({
            'status': 'success',
            'report': report,
            'folk_name': name,
            'timeline': timeline_data  # 新增：返回时间轴数据
        })

    except Exception as e:
        logger.error(f"生成报告时出错: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

if __name__ == "__main__":
    # 示例民间评论
    user_comment_folk = [
        "这首民谣真好听，旋律优美！",
        "我觉得这首歌的歌词很有深意。",
        "民间故事的情节很吸引人。",
        "这首民谣的演唱者声音很动人。"
    ]

    # 处理评论
    results_df = process_user_comment_folk(user_comment_folk)
    logger.info(f"民间评论情感分析完成，结果如下：\n{results_df}")

    # 运行批量情感分析
    sentiments_all()
