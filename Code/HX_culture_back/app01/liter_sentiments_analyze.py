from transformers import pipeline
import pandas as pd
import logging
import pymysql
from django.http import JsonResponse

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

def get_folk_sentiment_label(text):
    """获取民俗文学评论的情感标签和得分"""
    try:
        results = distilled_student_sentiment_classifier(text)[0]
        max_score_label = max(results, key=lambda x: x['score'])
        return max_score_label['label'], max_score_label['score']
    except Exception as e:
        logger.error(f"处理民俗评论文本时出错: {text}. 错误信息: {str(e)}")
        return 'error', 0.0

def process_folk_comments(comments_list):
    """处理民俗文学评论列表并返回带标签的DataFrame"""
    results = []
    for comment in comments_list:
        label, score = get_folk_sentiment_label(comment)
        results.append({
            'comment': comment,
            'sentiment': label,
            'confidence': score
        })
    return pd.DataFrame(results)

def sentiments_all():
    """对所有文学评论进行情感分析并更新数据库"""
    try:
        # 建立数据库连接，添加超时设置
        conn = pymysql.connect(
            host='120.233.26.237', 
            port=15320, 
            user='root', 
            passwd='kissme77',
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
        cursor.execute("SELECT comment_id, comment_text FROM user_comment_literature WHERE sentiment IS NULL")
        comments = cursor.fetchall()
        
        processed_count = 0
        
        for comment in comments:
            try:
                sentiment_label, confidence = get_folk_sentiment_label(comment['comment_text'])
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
                        host='120.233.26.237', 
                        port=15320, 
                        user='root', 
                        passwd='kissme77',
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
    literature_name = request.GET.get('liter_name')
    try:
        conn = pymysql.connect(
            host='120.233.26.237', 
            port=15320, 
            user='root', 
            passwd='kissme77',
            db='hx_cultural_transmission_sys',
            charset='utf8'
        )
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 首先获取文学作品ID
        literature_id = cursor.execute(
            "SELECT liter_id FROM literature WHERE liter_name=%s",
            (literature_name,)
        )
        
        # 获取该文学作品的所有评论
        sql_query = "SELECT comment_text FROM user_comment_literature WHERE liter_id=%s"
        effect_row = cursor.execute(sql_query, (literature_id,))
        comment_list = cursor.fetchall()
        
        # 提取评论文本
        comment_list = [comment['comment_text'] for comment in comment_list]
        
        # 处理评论
        results = process_folk_comments(comment_list)
        
        cursor.close()
        conn.close()
        
        # 将DataFrame转换为列表以便JSON序列化
        results_list = results.to_dict('records')
        
        return JsonResponse(results_list, safe=False)
        
    except Exception as e:
        logger.error(f"处理文学评论情感分析时出错: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

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
    results_df = process_folk_comments(folk_comments)
    logger.info(f"民俗评论情感分析完成，结果如下：\n{results_df}")
    
    # 运行批量情感分析
    sentiments_all()
