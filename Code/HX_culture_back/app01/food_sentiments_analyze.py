# from transformers import pipeline
import pandas as pd
import logging
import pymysql
import json
from django.http import JsonResponse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 初始化情感分析模型
# sentiment_classifier = pipeline(
#     model="lxyuan/distilbert-base-multilingual-cased-sentiments-student",
#     return_all_scores=True
# )

# def get_food_sentiment_label(text):
#     """获取食品评论的情感标签和得分"""
#     try:
#         max_length = 512
#         if len(text) > max_length:
#             text = text[:max_length]
#         results = sentiment_classifier(text)[0]
#         max_score_label = max(results, key=lambda x: x['score'])
#         return max_score_label['label'], max_score_label['score']
#     except Exception as e:
#         logger.error(f"处理食品评论文本时出错: {text}. 错误信息: {str(e)}")
#         return 'neutral', 0.0 # 或者 'error_processing', 0.0

# def process_food_comments(comments_list):
#     """处理食品评论列表并返回带标签的字典列表"""
#     results = []
#     for comment in comments_list:
#         label, score = get_food_sentiment_label(comment)
#         results.append({
#             'comment': comment,
#             'sentiment': label,
#             'confidence': score
#         })
#     return results

# def sentiments_all():
#     """对所有食品评论进行情感分析并更新数据库"""
#     try:
#         conn = pymysql.connect(
#             host='8.148.26.99',
#             port=3306,
#             user='root',
#             passwd='song',
#             db='hx_cultural_transmission_sys',
#             charset='utf8',
#             connect_timeout=10,
#             read_timeout=30,
#             write_timeout=30,
#             autocommit=True
#         )
#         cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

#         cursor.execute("SELECT comment_id, comment_text FROM user_comment_food WHERE sentiment IS NULL OR sentiment = ''")
#         comments = cursor.fetchall()

#         processed_count = 0

#         for comment in comments:
#             try:
#                 sentiment_label, confidence = get_food_sentiment_label(comment['comment_text'])
#                 logger.info(f"评论ID: {comment['comment_id']}, 情感标签: {sentiment_label}, 置信度: {confidence}")

#                 update_sql = """
#                     UPDATE user_comment_food 
#                     SET sentiment = %s, sentiment_confidence = %s 
#                     WHERE comment_id = %s
#                 """
#                 cursor.execute(update_sql, (sentiment_label, confidence, comment['comment_id']))
#                 processed_count += 1

#                 if processed_count % 10 == 0:
#                     logger.info(f"已处理 {processed_count} 条评论")

#             except pymysql.Error as e:
#                 logger.error(f"数据库操作出错 (评论ID: {comment['comment_id']}): {str(e)}")
#                 continue
#             except Exception as e:
#                 logger.error(f"处理评论时出错 (评论ID: {comment['comment_id']}): {str(e)}")
#                 continue

#         logger.info(f"所有食品评论的情感分析已完成，共处理 {processed_count} 条评论")

#     except Exception as e:
#         logger.error(f"情感分析过程中出错: {str(e)}")
#     finally:
#         if 'cursor' in locals():
#             cursor.close()
#         if 'conn' in locals() and conn.open:
#             conn.close()

# def sentiments_analyze(request):
#     """获取食品评论的情感分析"""
#     name = request.GET.get('name')
#     try:
#         conn = pymysql.connect(
#             host='8.148.26.99',
#             port=3306,
#             user='root',
#             passwd='song',
#             db='hx_cultural_transmission_sys',
#             charset='utf8'
#         )
#         cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

#         cursor.execute("SELECT food_id FROM food WHERE food_name=%s", (name,))
#         food_result = cursor.fetchone()

#         if not food_result:
#             return {
#                 'status': 'error',
#                 'message': f'未找到食品: {name}'
#             }

#         sql_query = "SELECT comment_text FROM user_comment_food WHERE food_id=%s"
#         cursor.execute(sql_query, (food_result['food_id'],))
#         comment_list = cursor.fetchall()

#         comment_list = [comment['comment_text'] for comment in comment_list]

#         results = process_food_comments(comment_list)

#         cursor.close()
#         conn.close()

#         results_list = results

#         return results_list

#     except Exception as e:
#         logger.error(f"处理食品评论情感分析时出错: {str(e)}")
#         return {
#             'status': 'error',
#             'message': str(e)
#         }

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
    """获取指定食品的情感分析统计结果 (按年月分组)"""
    conn = None
    cursor = None
    name = request.GET.get('name', '').strip()
    if not name:
        return JsonResponse({
            'status': 'error',
            'message': '食品名称不能为空'
        }, status=400)

    logger.info(f"(food_sentiments_total_count) 正在查询食品: {name}")

    try:
        conn = pymysql.connect(host='8.148.26.99', port=3306, user='root',
                             passwd='song', db='hx_cultural_transmission_sys',
                             charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 获取 food_id
        cursor.execute("SELECT food_id FROM food WHERE food_name = %s", (name,))
        result = cursor.fetchone()
        if not result:
            logger.warning(f"(food_sentiments_total_count) 未找到食品: {name}")
            return JsonResponse({
                'status': 'not_found',
                'message': f"未找到食品: {name}"
            }, status=404)
        
        food_id = result['food_id']
        logger.info(f"(food_sentiments_total_count) 找到食品ID: {food_id}")

        # SQL查询
        sql = """
        SELECT 
            YEAR(comment_time) AS year,
            MONTH(comment_time) AS month,
            sentiment,
            COUNT(*) AS comment_count,
            AVG(sentiment_confidence) AS sentiment_score,
            ROUND(COUNT(*) * 100.0 / (
                SELECT COUNT(*) 
                FROM user_comment_food 
                WHERE food_id = %s 
                AND YEAR(comment_time) = YEAR(ucf.comment_time) 
                AND MONTH(comment_time) = MONTH(ucf.comment_time)
            ), 2) as percentage
        FROM user_comment_food ucf
        WHERE food_id = %s
            AND sentiment IS NOT NULL
            AND sentiment != ''
            AND sentiment != 'error_processing'
        GROUP BY 
            YEAR(comment_time), 
            MONTH(comment_time),
            sentiment
        ORDER BY year, month, sentiment;
        """
        
        cursor.execute(sql, (food_id, food_id))
        results = cursor.fetchall()

        if not results:
            logger.info(f"(food_sentiments_total_count) 食品 {name} (ID: {food_id}) 暂无有效评论数据")
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
        logger.error(f"(food_sentiments_total_count) 数据库错误 for {name}: {str(db_err)}")
        return JsonResponse({
            'status': 'error',
            'message': f"数据库错误: {str(db_err)}"
        }, status=500)
    except Exception as e:
        logger.error(f"(food_sentiments_total_count) 未知错误 for {name}: {str(e)}")
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
    """根据食品名称获取情感分析时间序列结果"""
    try:
        name = request.GET.get('name', '').strip()
        if not name:
            return JsonResponse({
                'status': 'error',
                'message': '食品名称不能为空'
            }, status=400)

        logger.info(f"正在查询食品: {name}")

        conn = pymysql.connect(host='8.148.26.99', port=3306, user='root',
                             passwd='song', db='hx_cultural_transmission_sys',
                             charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        cursor.execute("SELECT food_id FROM food WHERE food_name = %s LIMIT 1", (name,))
        food_result = cursor.fetchone()

        if not food_result:
            return JsonResponse({
                'status': 'error',
                'message': f'未找到食品: {name}'
            }, status=404)

        food_id = food_result['food_id']
        logger.info(f"找到食品ID: {food_id}")

        comment_sql = """
            SELECT 
                sentiment, 
                sentiment_confidence, 
                SUBSTRING_INDEX(LEFT(comment_time, 7), '-', 1) as year,
                SUBSTRING_INDEX(LEFT(comment_time, 7), '-', -1) as month
            FROM user_comment_food 
            WHERE food_id = %s AND sentiment IS NOT NULL AND sentiment != ''
            ORDER BY comment_time
        """
        cursor.execute(comment_sql, (food_id,))
        results = cursor.fetchall()

        if not results:
            return JsonResponse({
                'status': 'success',
                'data': [],
                'food_info': {
                    'name': name,
                    'id': food_id
                },
                'message': '该食品暂无评论数据'
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
            'food_info': {
                'name': name,
                'id': food_id
            }
        })

    except Exception as e:
        logger.error(f"处理食品 {name} 的情感分析时出错: {str(e)}")
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
    """获取食品评论的情感分析报告"""
    try:
        food_name = request.GET.get('name', '').strip()
        if not food_name:
            return JsonResponse({
                'status': 'error',
                'message': '食品名称不能为空'
            }, status=400)

        logger.info(f"正在获取食品 {food_name} 的情感分析报告")

        conn = pymysql.connect(host='8.148.26.99', port=3306, user='root',
                              passwd='song', db='hx_cultural_transmission_sys',
                              charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        try:
            # 首先获取food_id
            cursor.execute("SELECT food_id FROM food WHERE food_name = %s", (food_name,))
            food_result = cursor.fetchone()
            
            if not food_result:
                logger.error(f"未找到食品: {food_name}")
                return JsonResponse({
                    'status': 'error',
                    'message': f'未找到食品: {food_name}'
                }, status=404)
            
            food_id = food_result['food_id']
            logger.info(f"找到食品ID: {food_id}")

            # 查询tag_id
            cursor.execute("SELECT tag_id FROM tag WHERE tag_name = %s", (food_name,))
            tag_result = cursor.fetchone()

            if not tag_result:
                logger.error(f"未找到食品对应的标签: {food_name}")
                return JsonResponse({
                    'status': 'error',
                    'message': f'未找到食品对应的标签: {food_name}'
                }, status=404)

            tag_id = tag_result['tag_id']
            logger.info(f"找到标签ID: {tag_id}")

            # 查询报告内容（包括中英文）
            cursor.execute("SELECT content, en_content FROM report WHERE tag_id = %s", (tag_id,))
            report_result = cursor.fetchone()

            if not report_result:
                logger.error(f"未找到食品的报告: {food_name}")
                return JsonResponse({
                    'status': 'error',
                    'message': f'未找到食品的报告: {food_name}'
                }, status=404)

            # 获取时间线数据
            timeline_sql = """
            SELECT 
                CONCAT(YEAR(comment_time), '-', LPAD(MONTH(comment_time), 2, '0')) as date,
                sentiment,
                COUNT(*) as count,
                AVG(sentiment_confidence) as score
            FROM user_comment_food
            WHERE food_id = %s
                AND sentiment IS NOT NULL
                AND sentiment != ''
            GROUP BY YEAR(comment_time), MONTH(comment_time), sentiment
            ORDER BY YEAR(comment_time), MONTH(comment_time), sentiment
            """
            
            cursor.execute(timeline_sql, (food_id,))
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
                'food_name': food_name
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

if __name__ == "__main__":
    # 示例食品评论
    food_comments = [
        "这道菜真好吃，味道鲜美！",
        "我觉得这家餐厅的服务态度很差。",
        "食物的分量很足，性价比高。",
        "这道菜的味道一般，没有特别惊艳的地方。"
    ]

    # 处理评论
    results_df = process_food_comments(food_comments)
    logger.info(f"食品评论情感分析完成，结果如下：\n{results_df}")

    # 运行批量情感分析
    sentiments_all()
