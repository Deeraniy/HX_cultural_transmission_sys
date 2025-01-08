import pymysql
import logging
from transformers import pipeline
import time
import signal
from functools import wraps
import random
import threading

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def init_sentiment_classifier():
    """初始化情感分析模型"""
    try:
        classifier = pipeline(
            model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", 
            return_all_scores=True
        )
        return classifier
    except Exception as e:
        logger.error(f"初始化情感分析模型失败: {str(e)}")
        raise

class TimeoutError(Exception):
    pass

def timeout(seconds):
    """使用 threading.Timer 实现的超时装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = []
            error = []
            
            def target():
                try:
                    result.append(func(*args, **kwargs))
                except Exception as e:
                    error.append(e)
            
            thread = threading.Thread(target=target)
            thread.daemon = True
            thread.start()
            thread.join(seconds)
            
            if thread.is_alive():
                raise TimeoutError(f"函数执行超过 {seconds} 秒")
            
            if error:
                raise error[0]
                
            return result[0] if result else None
            
        return wrapper
    return decorator

@timeout(10)  # 设置10秒超时
def get_sentiment_label(text):
    """获取文本的情感标签和置信度"""
    try:
        results = distilled_student_sentiment_classifier(text)
        sentiment_scores = results[0]
        max_sentiment = max(sentiment_scores, key=lambda x: x['score'])
        return max_sentiment['label'], max_sentiment['score']
    except Exception as e:
        logger.error(f"情感分析出错: {str(e)}")
        return None, None

def process_single_token(token, conn, cursor, max_retries=3):
    """处理单个词语，带有重试机制"""
    retry_count = 0
    while retry_count < max_retries:
        try:
            # 进行情感分析
            sentiment_label, confidence = get_sentiment_label(token['token_name'])
            
            if sentiment_label and confidence:
                # 更新数据库
                update_sql = """
                    UPDATE liter_token 
                    SET sentiment = %s, sentiment_confidence = %s 
                    WHERE token_id = %s
                """
                cursor.execute(update_sql, (sentiment_label, confidence, token['token_id']))
                conn.commit()
                logger.info(f"成功处理词语: {token['token_name']}, 情感: {sentiment_label}, 置信度: {confidence:.4f}")
                return True
            else:
                retry_count += 1
                delay = (2 ** retry_count) + random.random()  # 指数退避 + 随机延迟
                logger.warning(f"处理词语 {token['token_name']} 失败，{delay:.1f}秒后进行第{retry_count + 1}次重试")
                time.sleep(delay)
        
        except TimeoutError:
            retry_count += 1
            delay = (2 ** retry_count) + random.random()
            logger.warning(f"处理词语 {token['token_name']} 超时，{delay:.1f}秒后进行第{retry_count + 1}次重试")
            time.sleep(delay)
        
        except Exception as e:
            retry_count += 1
            delay = (2 ** retry_count) + random.random()
            logger.error(f"处理词语 {token['token_name']} 出错: {str(e)}，{delay:.1f}秒后进行第{retry_count + 1}次重试")
            time.sleep(delay)
    
    logger.error(f"处理词语 {token['token_name']} 失败，已达到最大重试次数")
    return False

def analyze_token_sentiments():
    """对liter_token表中的词语进行情感分析"""
    try:
        conn = pymysql.connect(
            host='120.233.26.237', 
            port=15320, 
            user='root', 
            passwd='kissme77',
            db='hx_cultural_transmission_sys', 
            charset='utf8',
            connect_timeout=30
        )
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        cursor.execute("""
            SELECT token_id, token_name 
            FROM liter_token 
            WHERE sentiment IS NULL
        """)
        tokens = cursor.fetchall()

        if not tokens:
            logger.info("没有需要分析的词语")
            return

        total_tokens = len(tokens)
        logger.info(f"开始处理 {total_tokens} 个词语的情感分析")
        processed_count = 0
        error_count = 0

        for token in tokens:
            logger.info(f"正在处理第 {processed_count + 1}/{total_tokens} 个词语: {token['token_name']}")
            
            # 处理单个词语
            if process_single_token(token, conn, cursor):
                processed_count += 1
            else:
                error_count += 1
            
            # 每100个词语重新连接数据库
            if processed_count % 100 == 0 and processed_count > 0:
                cursor.close()
                conn.close()
                conn = pymysql.connect(
                    host='120.233.26.237', 
                    port=15320, 
                    user='root', 
                    passwd='kissme77',
                    db='hx_cultural_transmission_sys', 
                    charset='utf8',
                    connect_timeout=30
                )
                cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
                logger.info("数据库连接已刷新")

        logger.info(f"""
        情感分析完成！
        总词语数: {total_tokens}
        成功处理: {processed_count}
        失败数量: {error_count}
        成功率: {(processed_count/total_tokens*100):.2f}%
        """)

    except Exception as e:
        logger.error(f"情感分析过程中出错: {str(e)}")
        raise
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    try:
        # 初始化情感分析模型
        distilled_student_sentiment_classifier = init_sentiment_classifier()
        # 开始分析
        analyze_token_sentiments()
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
