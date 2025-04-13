from transformers import pipeline
import pandas as pd
import logging
import pymysql
import json
from django.http import JsonResponse
from zhipuai import ZhipuAI

# 初始化 zhipuai 客户端
client = ZhipuAI(api_key="1af4f35363ea97ed269ee3099c04f7f3.3AGroi22UtegCtjf")

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

def get_literature_sentiment_label(text):
    """获取文学评论的情感标签和得分"""
    try:
        # 如果文本过长，截取前512个字符
        max_length = 512
        if len(text) > max_length:
            text = text[:max_length]

        # 使用 zhipuai 进行情感分析
        response = client.chat.completions.create(
            model="glm-4",
            messages=[
                {"role": "system", "content": "你是一个专业的情感分析助手，请分析以下文本的情感倾向，只返回 positive、neutral 或 negative 中的一个词。"},
                {"role": "user", "content": text}
            ],
            temperature=0.1
        )
        
        sentiment = response.choices[0].message.content.strip().lower()
        confidence = 0.9  # 由于是确定性输出，设置较高的置信度
        
        return sentiment, confidence
    except Exception as e:
        logger.error(f"处理文学评论文本时出错: {text}. 错误信息: {str(e)}")
        return 'neutral', 0.0

def process_literature_comments(comments_list):
    """处理文学评论列表并返回带标签的字典列表"""
    results = []
    for comment in comments_list:
        label, score = get_literature_sentiment_label(comment)
        results.append({
            'comment': comment,
            'sentiment': label,
            'confidence': score
        })
    return results

def sentiments_all():
    """对所有文学评论进行情感分析并更新数据库"""
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
        cursor.execute("SELECT comment_id, comment_text FROM user_comment_literature WHERE sentiment IS NULL OR sentiment = ''")
        comments = cursor.fetchall()

        processed_count = 0

        for comment in comments:
            try:
                sentiment_label, confidence = get_literature_sentiment_label(comment['comment_text'])
                logger.info(f"评论ID: {comment['comment_id']}, 情感标签: {sentiment_label}, 置信度: {confidence}")

                # 更新数据库
                update_sql = """
                    UPDATE user_comment_literature 
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

        logger.info(f"所有文学评论的情感分析已完成，共处理 {processed_count} 条评论")

    except Exception as e:
        logger.error(f"情感分析过程中出错: {str(e)}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.open:
            conn.close()

def sentiments_analyze(request):
    """获取文学作品的评论情感分析"""
    name = request.GET.get('name')
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

        # 首先获取文学作品ID
        literature_id = cursor.execute(
            "SELECT liter_id FROM literature WHERE liter_name=%s",
            (name,)
        )

        # 获取该文学作品的所有评论
        sql_query = "SELECT comment_text FROM user_comment_literature WHERE liter_id=%s"
        effect_row = cursor.execute(sql_query, (literature_id,))
        comment_list = cursor.fetchall()

        # 提取评论文本
        comment_list = [comment['comment_text'] for comment in comment_list]

        # 处理评论
        results = process_literature_comments(comment_list)

        cursor.close()
        conn.close()

        # 将DataFrame转换为列表以便JSON序列化
        results_list = results

        return results_list

    except Exception as e:
        logger.error(f"处理文学评论情感分析时出错: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }

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

def sentiments_result(request):
    """根据文学作品名称获取情感分析时间序列结果"""
    try:
        name = request.GET.get('name', '').strip()
        if not name:
            return JsonResponse({
                'status': 'error',
                'message': '文学作品名称不能为空'
            }, status=400)

        logger.info(f"正在查询文学作品: {name}")

        conn = pymysql.connect(host='8.148.26.99', port=3306, user='root',
                             passwd='song', db='hx_cultural_transmission_sys',
                             charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        cursor.execute("SELECT liter_id FROM literature WHERE liter_name = %s LIMIT 1", (name,))
        liter_result = cursor.fetchone()

        if not liter_result:
            return JsonResponse({
                'status': 'error',
                'message': f'未找到文学作品: {name}'
            }, status=404)

        liter_id = liter_result['liter_id']
        logger.info(f"找到文学作品ID: {liter_id}")

        comment_sql = """
            SELECT 
                sentiment, 
                sentiment_confidence, 
                SUBSTRING_INDEX(LEFT(comment_time, 7), '-', 1) as year,
                SUBSTRING_INDEX(LEFT(comment_time, 7), '-', -1) as month
            FROM user_comment_literature 
            WHERE liter_id = %s AND sentiment IS NOT NULL AND sentiment != ''
            ORDER BY comment_time
        """
        cursor.execute(comment_sql, (liter_id,))
        results = cursor.fetchall()

        if not results:
            return JsonResponse({
                'status': 'success',
                'data': [],
                'literature_info': {
                    'name': name,
                    'id': liter_id
                },
                'message': '该文学作品暂无评论数据'
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
            'literature_info': {
                'name': name,
                'id': liter_id
            }
        })

    except Exception as e:
        logger.error(f"处理文学作品 {name} 的情感分析时出错: {str(e)}")
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
    """获取文学作品评论的情感分析报告"""
    try:
        liter_name = request.GET.get('name', '').strip()
        if not liter_name:
            return JsonResponse({
                'status': 'error',
                'message': '文学作品名称不能为空'
            }, status=400)

        logger.info(f"正在获取文学作品 {liter_name} 的情感分析报告")

        conn = pymysql.connect(host='8.148.26.99', port=3306, user='root',
                              passwd='song', db='hx_cultural_transmission_sys',
                              charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        try:
            # 首先获取liter_id
            cursor.execute("SELECT liter_id FROM literature WHERE liter_name = %s", (liter_name,))
            liter_result = cursor.fetchone()
            
            if not liter_result:
                logger.error(f"未找到文学作品: {liter_name}")
                return JsonResponse({
                    'status': 'error',
                    'message': f'未找到文学作品: {liter_name}'
                }, status=404)
            
            liter_id = liter_result['liter_id']
            logger.info(f"找到文学作品ID: {liter_id}")

            # 查询tag_id
            cursor.execute("SELECT tag_id FROM tag WHERE tag_name = %s", (liter_name,))
            tag_result = cursor.fetchone()

            if not tag_result:
                logger.error(f"未找到文学作品对应的标签: {liter_name}")
                return JsonResponse({
                    'status': 'error',
                    'message': f'未找到文学作品对应的标签: {liter_name}'
                }, status=404)

            tag_id = tag_result['tag_id']
            logger.info(f"找到标签ID: {tag_id}")

            # 查询报告内容（包括中英文）
            cursor.execute("SELECT content, en_content FROM report WHERE tag_id = %s", (tag_id,))
            report_result = cursor.fetchone()

            if not report_result:
                logger.error(f"未找到文学作品的报告: {liter_name}")
                return JsonResponse({
                    'status': 'error',
                    'message': f'未找到文学作品的报告: {liter_name}'
                }, status=404)

            # 获取时间线数据
            timeline_sql = """
            SELECT 
                CONCAT(YEAR(comment_time), '-', LPAD(MONTH(comment_time), 2, '0')) as date,
                sentiment,
                COUNT(*) as count,
                AVG(sentiment_confidence) as score
            FROM user_comment_literature
            WHERE liter_id = %s
                AND sentiment IS NOT NULL
                AND sentiment != ''
            GROUP BY YEAR(comment_time), MONTH(comment_time), sentiment
            ORDER BY YEAR(comment_time), MONTH(comment_time), sentiment
            """
            
            cursor.execute(timeline_sql, (liter_id,))
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
                'liter_name': liter_name
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

def sentiments_result_total_count(request):
    """获取指定文学作品的情感分析统计结果 (按年月分组)"""
    conn = None
    cursor = None
    name = request.GET.get('name', '').strip()
    if not name:
        return JsonResponse({
            'status': 'error',
            'message': '文学作品名称不能为空'
        }, status=400)

    logger.info(f"(liter_sentiments_total_count) 正在查询文学作品: {name}")

    try:
        conn = pymysql.connect(host='8.148.26.99', port=3306, user='root',
                             passwd='song', db='hx_cultural_transmission_sys',
                             charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 获取 liter_id
        cursor.execute("SELECT liter_id FROM literature WHERE liter_name = %s", (name,))
        result = cursor.fetchone()
        if not result:
            logger.warning(f"(liter_sentiments_total_count) 未找到文学作品: {name}")
            return JsonResponse({
                'status': 'not_found',
                'message': f"未找到文学作品: {name}"
            }, status=404)
        
        liter_id = result['liter_id']
        logger.info(f"(liter_sentiments_total_count) 找到文学作品ID: {liter_id}")

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
                FROM user_comment_literature 
                WHERE liter_id = %s 
                AND YEAR(comment_time) = YEAR(ucl.comment_time) 
                AND MONTH(comment_time) = MONTH(ucl.comment_time)
            ), 2) as percentage
        FROM user_comment_literature ucl
        WHERE liter_id = %s
            AND sentiment IS NOT NULL
            AND sentiment != ''
            AND sentiment != 'error_processing'
        GROUP BY 
            YEAR(comment_time), 
            MONTH(comment_time),
            sentiment
        ORDER BY year, month, sentiment;
        """
        
        cursor.execute(sql, (liter_id, liter_id))
        results = cursor.fetchall()

        if not results:
            logger.info(f"(liter_sentiments_total_count) 文学作品 {name} (ID: {liter_id}) 暂无有效评论数据")
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
        logger.error(f"(liter_sentiments_total_count) 数据库错误 for {name}: {str(db_err)}")
        return JsonResponse({
            'status': 'error',
            'message': f"数据库错误: {str(db_err)}"
        }, status=500)
    except Exception as e:
        logger.error(f"(liter_sentiments_total_count) 未知错误 for {name}: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f"未知错误: {str(e)}"
        }, status=500)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# 使用示例
if __name__ == "__main__":
    # 民俗文学相关评论示例
    folk_comments = [
        "这个民间故事非常有趣，展现了丰富的文化内涵",
        "传统习俗的传承方式很独特，令人印象深刻",
        "这个民俗活动的意义似乎有点模糊",
        "民间文学的表现形式太过陈旧了"
    ]

    # 处理评论
    results_df = process_literature_comments(folk_comments)
    logger.info(f"民俗评论情感分析完成，结果如下：\n{results_df}")

    # 运行批量情感分析
    sentiments_all()
