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
    """过滤非遗民俗相关词语"""
    with open("stopwords.txt", 'r', encoding='utf-8') as f:
        stopwords = set([line.strip() for line in f])
    
    return len(word) >= min_length and word not in stopwords

def get_db_connection():
    """获取数据库连接"""
    return pymysql.connect(
        host='120.233.26.237', 
        port=15320, 
        user='root', 
        passwd='kissme77', 
        db='hx_cultural_transmission_sys', 
        charset='utf8',
        connect_timeout=10,
        read_timeout=30,
        write_timeout=30
    )

def has_processed_tokens(folk_id):
    """检查folk_id是否已经处理过非遗民俗相关的词语"""
    conn = get_db_connection()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT COUNT(*) as count FROM folk_token WHERE folk_id = %s", (folk_id,))
        result = cursor.fetchone()
        return result['count'] > 0
    finally:
        cursor.close()
        conn.close()

def process_folk_tokens(folk_name):
    """处理非遗民俗评论分词并更新数据库"""
    try:
        if not folk_name:
            logger.error("非遗民俗名称不能为空")
            return False

        # 获取folk_id的连接
        conn = get_db_connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 获取folk_id
        folk_sql = "SELECT folk_id FROM folk WHERE folk_name = %s"
        cursor.execute(folk_sql, (folk_name,))
        folk_result = cursor.fetchone()
        
        if not folk_result:
            logger.error(f'未找到非遗民俗: {folk_name}')
            return False
        
        folk_id = folk_result['folk_id']
        logger.info(f"处理非遗民俗: {folk_name} (ID: {folk_id})")

        # 检查是否已经处理过
        if has_processed_tokens(folk_id):
            logger.info(f"非遗民俗 {folk_name} (ID: {folk_id}) 已经处理过，跳过。")
            return True

        # 获取评论的连接
        comment_sql = "SELECT comment_text FROM user_comment_folk WHERE folk_id = %s"
        cursor.execute(comment_sql, (folk_id,))
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
                process_word_batch(word_batch, folk_id)
                word_batch = []
                logger.info(f"已处理 {total_words} 个词语")

        # 处理剩余的词语
        if word_batch:
            process_word_batch(word_batch, folk_id)
            
        logger.info(f"处理完成，共处理 {len(comments)} 条评论，{total_words} 个词语")
        return True

    except Exception as e:
        logger.error(f"处理分词时出错: {str(e)}")
        return False
    finally:
        cursor.close()
        conn.close()

def process_all_folks():
    """处理所有非遗民俗"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 查询所有非遗民俗
        cursor.execute("SELECT folk_name FROM folk")
        folks = cursor.fetchall()

        for folk in folks:
            folk_name = folk['folk_name']
            logger.info(f"正在处理非遗民俗: {folk_name}")
            process_folk_tokens(folk_name)

    except Exception as e:
        logger.error(f"处理非遗民俗时出错: {str(e)}")
    finally:
        cursor.close()
        conn.close()

def process_word_batch(words, folk_id):
    """处理一批非遗民俗相关词语"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        
        for word in words:
            try:
                # 检查词语是否存在
                check_sql = """
                    SELECT token_id, count 
                    FROM folk_token 
                    WHERE token_name = %s AND folk_id = %s
                """
                cursor.execute(check_sql, (word, folk_id))
                token_result = cursor.fetchone()
                
                if token_result:
                    # 更新计数
                    update_sql = """
                        UPDATE folk_token 
                        SET count = count + 1 
                        WHERE token_id = %s
                    """
                    cursor.execute(update_sql, (token_result['token_id'],))
                else:
                    # 插入新词
                    insert_sql = """
                        INSERT INTO folk_token (token_name, count, folk_id) 
                        VALUES (%s, 1, %s)
                    """
                    cursor.execute(insert_sql, (word, folk_id))
                    
            except Exception as e:
                logger.error(f"处理词语 {word} 时出错: {str(e)}")
                continue
                
        conn.commit()
        
    except Exception as e:
        logger.error(f"处理词语批次时出错: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def get_word_frequency(request):
    """获取非遗民俗相关词语频率以及情感"""
    try:
        folk_name = request.GET.get('name')
        if not folk_name:
            return JsonResponse({
                'status': 'error',
                'message': '非遗民俗名称不能为空'
            }, status=400)

        # 获取数据库连接
        conn = get_db_connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 获取folk_id
        folk_sql = "SELECT folk_id FROM folk WHERE folk_name = %s"
        cursor.execute(folk_sql, (folk_name,))
        folk_result = cursor.fetchone()

        if not folk_result:
            return JsonResponse({
                'status': 'error',
                'message': f'未找到非遗民俗: {folk_name}'
            }, status=404)

        folk_id = folk_result['folk_id']
        logger.info(f"查询非遗民俗 {folk_name} (ID: {folk_id}) 的词频")

        # 查询中间40个高频词
        frequency_sql = """
            SELECT token_name as word, count as frequency, sentiment
            FROM folk_token 
            WHERE folk_id = %s 
            ORDER BY count DESC 
            LIMIT 30 OFFSET 40
        """
        cursor.execute(frequency_sql, (folk_id,))
        words = cursor.fetchall()

        logger.info(f"找到 {len(words)} 个高频词")

        return JsonResponse(words, safe=False)

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
    process_all_folks()