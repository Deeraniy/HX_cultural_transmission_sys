import jieba
import pymysql
import logging
import random
import time
from django.http import JsonResponse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 关闭jieba的日志输出
jieba.setLogLevel(logging.INFO)

def filter_words(word, min_length=2):
    """过滤文学相关词语"""
    with open("stopwords.txt", 'r', encoding='utf-8') as f:
        stopwords = set([line.strip() for line in f])
    
    return len(word) >= min_length and word not in stopwords

def get_db_connection():
    """获取数据库连接"""
    return pymysql.connect(
        host='60.215.128.117', 
        port=15320, 
        user='root', 
        passwd='kissme77', 
        db='hx_cultural_transmission_sys', 
        charset='utf8',
        connect_timeout=10,
        read_timeout=30,
        write_timeout=30
    )

def has_processed_tokens(liter_id):
    """检查liter_id是否已经处理过文学相关的词语"""
    conn = get_db_connection()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT COUNT(*) as count FROM liter_token WHERE liter_id = %s", (liter_id,))
        result = cursor.fetchone()
        return result['count'] > 0
    finally:
        cursor.close()
        conn.close()

def process_liter_tokens(literature_name):
    """处理文学作品评论分词并更新数据库"""
    try:
        if not literature_name:
            logger.error("文学作品名称不能为空")
            return False

        # 获取liter_id的连接
        conn = get_db_connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 获取liter_id
        liter_sql = "SELECT liter_id FROM literature WHERE liter_name = %s"
        cursor.execute(liter_sql, (literature_name,))
        liter_result = cursor.fetchone()
        
        if not liter_result:
            logger.error(f'未找到文学作品: {literature_name}')
            return False
        
        liter_id = liter_result['liter_id']
        logger.info(f"处理文学作品: {literature_name} (ID: {liter_id})")

        # 检查是否已经处理过
        if has_processed_tokens(liter_id):
            logger.info(f"文学作品 {literature_name} (ID: {liter_id}) 已经处理过，跳过。")
            return True

        # 获取评论的连接
        comment_sql = "SELECT comment_text FROM user_comment_literature WHERE liter_id = %s"
        cursor.execute(comment_sql, (liter_id,))
        comments = cursor.fetchall()

        # 每100条评论提交一次事务
        batch_size = 100
        total_words = 0
        word_batch = []

        # 先收集所有词语
        for comment in comments:
            words = jieba.cut(comment['comment_text'])
            filtered_words = [word for word in words if filter_words(word)]
            
            if len(filtered_words) > 10:
                filtered_words = random.sample(filtered_words, 10)
            
            word_batch.extend(filtered_words)
            total_words += len(filtered_words)
            
            # 当批次达到大小时处理
            if len(word_batch) >= batch_size:
                process_word_batch(word_batch, liter_id)
                word_batch = []
                logger.info(f"已处理 {total_words} 个词语")

        # 处理剩余的词语
        if word_batch:
            process_word_batch(word_batch, liter_id)
            
        logger.info(f"处理完成，共处理 {len(comments)} 条评论，{total_words} 个词语")
        return True

    except pymysql.Error as db_error:
        logger.error(f"数据库操作时出错: {str(db_error)}")
        return False
    except Exception as e:
        logger.error(f"处理分词时出错: {str(e)}")
        return False
    finally:
        cursor.close()
        conn.close()

def process_all_literatures():
    """处理所有文学作品"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 查询所有文学作品
        cursor.execute("SELECT liter_name FROM literature")
        literatures = cursor.fetchall()

        for liter in literatures:
            literature_name = liter['liter_name']
            logger.info(f"正在处理文学作品: {literature_name}")
            process_liter_tokens(literature_name)

    except pymysql.Error as db_error:
        logger.error(f"数据库操作时出错: {str(db_error)}")
    except Exception as e:
        logger.error(f"处理文学作品时出错: {str(e)}")
    finally:
        cursor.close()
        conn.close()

def process_word_batch(words, liter_id):
    """处理一批文学相关词语"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        
        for word in words:
            try:
                # 检查词语是否存在
                check_sql = """
                    SELECT token_id, count 
                    FROM liter_token 
                    WHERE token_name = %s AND liter_id = %s
                """
                cursor.execute(check_sql, (word, liter_id))
                token_result = cursor.fetchone()
                
                if token_result:
                    # 更新计数
                    update_sql = """
                        UPDATE liter_token 
                        SET count = count + 1 
                        WHERE token_id = %s
                    """
                    cursor.execute(update_sql, (token_result['token_id'],))
                else:
                    # 插入新词
                    insert_sql = """
                        INSERT INTO liter_token (token_name, count, liter_id) 
                        VALUES (%s, 1, %s)
                    """
                    cursor.execute(insert_sql, (word, liter_id))
                    
            except pymysql.Error as db_error:
                logger.error(f"数据库操作时出错 (词语: {word}): {str(db_error)}")
                continue
            except Exception as e:
                logger.error(f"处理词语 {word} 时出错: {str(e)}")
                continue
                
        conn.commit()
        
    except pymysql.Error as db_error:
        logger.error(f"处理词语批次时出错: {str(db_error)}")
        if 'conn' in locals():
            conn.rollback()
    except Exception as e:
        logger.error(f"处理词语批次时出错: {str(e)}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def get_word_frequency(request):
    """获取文学相关词语频率以及情感"""
    try:
        literature_name = request.GET.get('name')
        if not literature_name:
            logger.error("文学作品名称不能为空")
            return JsonResponse({
                'status': 'error',
                'message': '文学作品名称不能为空'
            }, status=400)

        logger.info(f"请求获取文学作品 '{literature_name}' 的词频")

        # 获取数据库连接
        conn = get_db_connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 获取liter_id
        liter_sql = "SELECT liter_id FROM literature WHERE liter_name = %s"
        cursor.execute(liter_sql, (literature_name,))
        liter_result = cursor.fetchone()

        if not liter_result:
            logger.error(f"未找到文学作品: {literature_name}")
            return JsonResponse({
                'status': 'error',
                'message': f'未找到文学作品: {literature_name}'
            }, status=404)

        liter_id = liter_result['liter_id']
        logger.info(f"查询文学作品 {literature_name} (ID: {liter_id}) 的词频")

        # 查询中间40个高频词
        frequency_sql = """
            SELECT token_name as word, count as frequency, sentiment
            FROM liter_token 
            WHERE liter_id = %s 
            ORDER BY count DESC 
            LIMIT 30 OFFSET 40
        """
        cursor.execute(frequency_sql, (liter_id,))
        words = cursor.fetchall()

        logger.info(f"找到 {len(words)} 个高频词")

        return JsonResponse({
            'status': 'success',
            'data': words
        }, safe=False)

    except pymysql.Error as db_error:
        logger.error(f"获取词频时数据库操作出错: {str(db_error)}")
        return JsonResponse({
            'status': 'error',
            'message': '数据库操作出错'
        }, status=500)
    except Exception as e:
        logger.error(f"获取词频时出错: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    process_all_literatures()