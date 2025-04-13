import os

# 禁用代理设置
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

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
        # 如果文本过长，截取前512个字符
        max_length = 512
        if len(text) > max_length:
            text = text[:max_length]

        results = distilled_student_sentiment_classifier(text)[0]  # 获取分析结果
        # 找出得分最高的标签
        max_score_label = max(results, key=lambda x: x['score'])
        return max_score_label['label'], max_score_label['score']
    except Exception as e:
        logger.error(f"处理文本时出错: {text}. 错误信息: {str(e)}")
        return 'neutral', 0.5  # 对于处理失败的情况返回中性评价

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
    name = request.GET.get('name')
    conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', passwd='song',
                           db='hx_cultural_transmission_sys',charset='utf8')

    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    spot_id=cursor.execute("SELECT spot_id FROM spot WHERE spot_name=%s",(name))
    sql_query = "SELECT content FROM user_comment_spot WHERE spot_id=%s"
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
    """对所有景点评论进行情感分析并更新数据库"""
    try:
        # 建立数据库连接，添加超时设置
        conn = pymysql.connect(
            host='8.148.26.99',
            port=3306,
            user='root',
            passwd='song',
            db='hx_cultural_transmission_sys',
            charset='utf8',
            connect_timeout=10,        # 连接超时
            read_timeout=30,           # 读取超时
            write_timeout=30,          # 写入超时
            autocommit=True            # 自动提交
        )
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 确保开始前没有未完成的事务
        conn.rollback()

        # 获取所有评论
        cursor.execute("SELECT comment_id, comment_text FROM user_comment_spot WHERE sentiment IS NULL OR sentiment = ''")
        comments = cursor.fetchall()

        processed_count = 0

        for comment in comments:
            try:
                sentiment_label, confidence = get_sentiment_label(comment['comment_text'])
                logger.info(f"评论ID: {comment['comment_id']}, 情感标签: {sentiment_label}, 置信度: {confidence}")

                # 更新数据库
                update_sql = """
                    UPDATE user_comment_spot 
                    SET sentiment = %s, sentiment_confidence = %s 
                    WHERE comment_id = %s
                """
                cursor.execute(update_sql, (sentiment_label, confidence, comment['comment_id']))
                processed_count += 1

                if processed_count % 10 == 0:  # 每10条记录输出一次进度
                    logger.info(f"已处理 {processed_count} 条评论")

            except pymysql.Error as e:
                logger.error(f"数据库操作出错 (评论ID: {comment['comment_id']}): {str(e)}")
                # 尝试重新连接
                if not conn.open:
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
            except Exception as e:
                logger.error(f"处理评论时出错 (评论ID: {comment['comment_id']}): {str(e)}")
                continue

        logger.info(f"所有景点评论的情感分析已完成，共处理 {processed_count} 条评论")

    except Exception as e:
        logger.error(f"情感分析过程中出错: {str(e)}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.open:
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
    """获取指定景点的情感分析统计结果 (按年月分组)"""
    conn = None
    cursor = None
    name = request.GET.get('name', '').strip()
    if not name:
        return JsonResponse({
            'status': 'error',
            'message': '景点名称不能为空'
        }, status=400)

    logger.info(f"(spot_sentiments_total_count) 正在查询景点: {name}")

    try:
        conn = pymysql.connect(host='8.148.26.99', port=3306, user='root',
                             passwd='song', db='hx_cultural_transmission_sys',
                             charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 获取 spot_id
        cursor.execute("SELECT spot_id FROM spot WHERE spot_name = %s", (name,))
        result = cursor.fetchone()
        if not result:
            logger.warning(f"(spot_sentiments_total_count) 未找到景点: {name}")
            return JsonResponse({
                'status': 'not_found',
                'message': f"未找到景点: {name}"
            }, status=404)
        
        spot_id = result['spot_id']
        logger.info(f"(spot_sentiments_total_count) 找到景点ID: {spot_id}")

        # SQL查询保持不变...
        sql = """
        SELECT 
            YEAR(comment_time) AS year,
            MONTH(comment_time) AS month,
            sentiment,
            COUNT(*) AS comment_count,
            AVG(sentiment_confidence) AS sentiment_score,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM user_comment_spot WHERE spot_id = %s AND YEAR(comment_time) = YEAR(ucs.comment_time) AND MONTH(comment_time) = MONTH(ucs.comment_time)), 2) as percentage
        FROM user_comment_spot ucs
        WHERE spot_id = %s
            AND sentiment IS NOT NULL
            AND sentiment != ''
            AND sentiment != 'error_processing'
        GROUP BY 
            YEAR(comment_time), 
            MONTH(comment_time),
            sentiment
        ORDER BY year, month, sentiment;
        """
        
        cursor.execute(sql, (spot_id, spot_id))
        results = cursor.fetchall()

        if not results:
            logger.info(f"(spot_sentiments_total_count) 景点 {name} (ID: {spot_id}) 暂无有效评论数据")
            return JsonResponse({
                'status': 'success',
                'data': [],
                'message': f"{name} 暂无评论数据"
            })

        # 处理结果
        processed_results = []
        for row in results:
            row['sentiment_score'] = float(row['sentiment_score']) if row['sentiment_score'] is not None else 0.0
            row['percentage'] = float(row['percentage']) if row['percentage'] is not None else 0.0
            processed_results.append({
                'year': row.get('year'),
                'month': row.get('month'),
                'sentiment': row.get('sentiment'),
                'comment_count': row.get('comment_count', 0),
                'sentiment_score': row['sentiment_score'],
                'percentage': row['percentage']
            })

        return JsonResponse({
            'status': 'success',
            'data': processed_results
        })

    except pymysql.Error as db_err:
        logger.error(f"(spot_sentiments_total_count) 数据库错误 for {name}: {str(db_err)}")
        return JsonResponse({
            'status': 'error',
            'message': f"数据库错误: {str(db_err)}"
        }, status=500)
    except Exception as e:
        logger.error(f"(spot_sentiments_total_count) 未知错误 for {name}: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f"未知错误: {str(e)}"
        }, status=500)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def sentiments_result(request):
    """根据景点名称获取情感分析时间序列结果"""
    try:
        name = request.GET.get('name', '').strip()
        if not name:
            return JsonResponse({
                'status': 'error',
                'message': '景点名称不能为空'
            }, status=400)

        logger.info(f"正在查询景点: {name}")

        conn = pymysql.connect(host='8.148.26.99', port=3306, user='root',
                             passwd='song', db='hx_cultural_transmission_sys',
                             charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        cursor.execute("SELECT spot_id FROM spot WHERE spot_name = %s LIMIT 1", (name,))
        spot_result = cursor.fetchone()

        if not spot_result:
            return JsonResponse({
                'status': 'error',
                'message': f'未找到景点: {name}'
            }, status=404)

        spot_id = spot_result['spot_id']
        logger.info(f"找到景点ID: {spot_id}")

        # 查询评论数据
        comment_sql = """
            SELECT 
                sentiment, 
                sentiment_confidence, 
                SUBSTRING_INDEX(LEFT(comment_time, 7), '-', 1) as year,
                SUBSTRING_INDEX(LEFT(comment_time, 7), '-', -1) as month
            FROM user_comment_spot 
            WHERE spot_id = %s AND sentiment IS NOT NULL AND sentiment != ''
            ORDER BY comment_time
        """
        cursor.execute(comment_sql, (spot_id,))
        results = cursor.fetchall()

        if not results:
            return JsonResponse({
                'status': 'success',
                'data': [],
                'spot_info': {
                    'name': name,
                    'id': spot_id
                },
                'message': '该景点暂无评论数据'
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

        # 按时间排序
        analysis_results.sort(key=lambda x: (x['year'], x['month']))

        return JsonResponse({
            'status': 'success',
            'data': analysis_results,
            'spot_info': {
                'name': name,
                'id': spot_id
            }
        })

    except Exception as e:
        logger.error(f"处理景点 {name} 的情感分析时出错: {str(e)}")
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
    """获取景点评论的情感分析报告"""
    try:
        spot_name = request.GET.get('name', '').strip()
        if not spot_name:
            return JsonResponse({
                'status': 'error',
                'message': '景点名称不能为空'
            }, status=400)

        logger.info(f"正在获取景点 {spot_name} 的情感分析报告")

        conn = pymysql.connect(host='8.148.26.99', port=3306, user='root',
                              passwd='song', db='hx_cultural_transmission_sys',
                              charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        try:
            # 首先获取spot_id
            cursor.execute("SELECT spot_id FROM spot WHERE spot_name = %s", (spot_name,))
            spot_result = cursor.fetchone()
            
            if not spot_result:
                logger.error(f"未找到景点: {spot_name}")
                return JsonResponse({
                    'status': 'error',
                    'message': f'未找到景点: {spot_name}'
                }, status=404)
            
            spot_id = spot_result['spot_id']
            logger.info(f"找到景点ID: {spot_id}")

            # 查询tag_id
            cursor.execute("SELECT tag_id FROM tag WHERE tag_name = %s", (spot_name,))
            tag_result = cursor.fetchone()

            if not tag_result:
                logger.error(f"未找到景点对应的标签: {spot_name}")
                return JsonResponse({
                    'status': 'error',
                    'message': f'未找到景点对应的标签: {spot_name}'
                }, status=404)

            tag_id = tag_result['tag_id']
            logger.info(f"找到标签ID: {tag_id}")

            # 查询报告内容（包括中英文）
            cursor.execute("SELECT content, en_content FROM report WHERE tag_id = %s", (tag_id,))
            report_result = cursor.fetchone()

            if not report_result:
                logger.error(f"未找到景点的报告: {spot_name}")
                return JsonResponse({
                    'status': 'error',
                    'message': f'未找到景点的报告: {spot_name}'
                }, status=404)

            # 获取时间线数据
            timeline_sql = """
            SELECT 
                CONCAT(YEAR(comment_time), '-', LPAD(MONTH(comment_time), 2, '0')) as date,
                sentiment,
                COUNT(*) as count,
                AVG(sentiment_confidence) as score
            FROM user_comment_spot
            WHERE spot_id = %s
                AND sentiment IS NOT NULL
                AND sentiment != ''
            GROUP BY YEAR(comment_time), MONTH(comment_time), sentiment
            ORDER BY YEAR(comment_time), MONTH(comment_time), sentiment
            """
            
            cursor.execute(timeline_sql, (spot_id,))
            timeline_results = cursor.fetchall()
            
            # 处理时间线数据
            timeline_data = []
            for row in timeline_results:
                timeline_data.append({
                    'date': row['date'],
                    'sentiment': row['sentiment'].lower(),
                    'count': int(row['count']),
                    'score': float(row['score']) if row['score'] is not None else 0.0
                })

            logger.info(f"成功获取时间线数据，共 {len(timeline_data)} 条记录")

            return JsonResponse({
                'status': 'success',
                'report': report_result['content'],
                'report_en': report_result['en_content'],
                'timeline': timeline_data,
                'spot_name': spot_name
            })

        except pymysql.Error as db_err:
            logger.error(f"数据库操作出错: {str(db_err)}")
            return JsonResponse({
                'status': 'error',
                'message': f"数据库错误: {str(db_err)}"
            }, status=500)
        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        logger.error(f"获取报告时出错: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

# 使用示例
if __name__ == "__main__":
    sentiments_all()
