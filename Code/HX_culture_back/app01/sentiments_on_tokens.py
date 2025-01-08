import pymysql
import logging
from transformers import pipeline
import time

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

def get_sentiment_label(text):
    """获取文本的情感标签和置信度"""
    try:
        results = distilled_student_sentiment_classifier(text)
        # 获取最高置信度的情感
        sentiment_scores = results[0]
        max_sentiment = max(sentiment_scores, key=lambda x: x['score'])
        return max_sentiment['label'], max_sentiment['score']
    except Exception as e:
        logger.error(f"情感分析出错: {str(e)}")
        return None, None

def analyze_token_sentiments():
    """对liter_token表中的词语进行情感分析"""
    try:
        # 建立数据库连接
        conn = pymysql.connect(
            host='120.233.26.237', 
            port=15320, 
            user='root', 
            passwd='kissme77',
            db='hx_cultural_transmission_sys', 
            charset='utf8',
            connect_timeout=30  # 增加连接超时时间
        )
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 获取所有未分析情感的词语
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
            try:
                logger.info(f"正在处理第 {processed_count + 1}/{total_tokens} 个词语: {token['token_name']}")
                
                # 进行情感分析
                sentiment_label, confidence = get_sentiment_label(token['token_name'])
                
                if sentiment_label and confidence:
                    try:
                        # 更新数据库
                        update_sql = """
                            UPDATE liter_token 
                            SET sentiment = %s, sentiment_confidence = %s 
                            WHERE token_id = %s
                        """
                        cursor.execute(update_sql, (sentiment_label, confidence, token['token_id']))
                        conn.commit()
                        
                        processed_count += 1
                        logger.info(f"成功处理词语: {token['token_name']}, 情感: {sentiment_label}, 置信度: {confidence:.4f}")
                        
                    except pymysql.Error as e:
                        logger.error(f"数据库更新失败: {str(e)}")
                        error_count += 1
                        conn.rollback()
                else:
                    logger.warning(f"词语 {token['token_name']} 情感分析返回空结果")
                    error_count += 1
                
                # 每100个词语重新连接一次数据库，避免连接超时
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
                
                # 添加短暂延迟避免请求过快
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"处理词语 {token['token_name']} (ID: {token['token_id']}) 时出错: {str(e)}")
                error_count += 1
                continue

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
