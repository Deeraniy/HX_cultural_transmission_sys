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
    """过滤词语"""
    with open("stopwords.txt", 'r', encoding='utf-8') as f:
        stopwords = set([line.strip() for line in f])
    
    return len(word) >= min_length and word not in stopwords

def process_literature_tokens(literature_name):
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
        
        cursor.close()
        conn.close()
        
        if not liter_result:
            logger.error(f'未找到文学作品: {literature_name}')
            return False
        
        liter_id = liter_result['liter_id']
        logger.info(f"处理文学作品: {literature_name} (ID: {liter_id})")

        # 获取评论的连接
        conn = get_db_connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 获取所有评论
        comment_sql = "SELECT comment_text FROM user_comment_literature WHERE liter_id = %s"
        cursor.execute(comment_sql, (liter_id,))
        comments = cursor.fetchall()
        
        cursor.close()
        conn.close()

        # 每100条评论提交一次事务
        batch_size = 100
        current_batch = 0
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

    except Exception as e:
        logger.error(f"处理分词时出错: {str(e)}")
        return False

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

def process_word_batch(words, liter_id):
    """处理一批词语"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        
        for word in words:
            try:
                # 检查词语是否存在
                check_sql = """
                    SELECT token_id, count 
                    FROM liter_token_test 
                    WHERE token_name = %s AND liter_id = %s
                """
                cursor.execute(check_sql, (word, liter_id))
                token_result = cursor.fetchone()
                
                if token_result:
                    # 更新计数
                    update_sql = """
                        UPDATE liter_token_test 
                        SET count = count + 1 
                        WHERE token_id = %s
                    """
                    cursor.execute(update_sql, (token_result['token_id'],))
                else:
                    # 插入新词
                    insert_sql = """
                        INSERT INTO liter_token_test (token_name, count, liter_id) 
                        VALUES (%s, 1, %s)
                    """
                    cursor.execute(insert_sql, (word, liter_id))
                    
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
    """获取词语频率以及情感"""
    try:
        liter_name = request.GET.get('name')
        if not liter_name:
            return JsonResponse({
                'status': 'error',
                'message': '文学作品名称不能为空'
            }, status=400)

        # 获取数据库连接
        conn = get_db_connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 获取liter_id
        liter_sql = "SELECT liter_id FROM literature WHERE liter_name = %s"
        cursor.execute(liter_sql, (liter_name,))
        liter_result = cursor.fetchone()

        if not liter_result:
            return JsonResponse({
                'status': 'error',
                'message': f'未找到文学作品: {liter_name}'
            }, status=404)

        liter_id = liter_result['liter_id']
        logger.info(f"查询文学作品 {liter_name} (ID: {liter_id}) 的词频")

        # 查询中间40个高频词
        frequency_sql = """
            SELECT token_name as word, count as frequency, sentiment
            FROM token 
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
        })

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
    try:
        # 连接数据库获取所有文学作品
        conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', 
                             passwd='kissme77', db='hx_cultural_transmission_sys', 
                             charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        
        # 获取所有文学作品
        literatures_sql = "SELECT liter_name FROM literature"
        cursor.execute(literatures_sql)
        literatures = [row['liter_name'] for row in cursor.fetchall()]
        
        logger.info(f"共找到 {len(literatures)} 个文学作品待处理")
        
        # 处理每个文学作品
        success_count = 0
        for i, liter_name in enumerate(literatures, 1):
            logger.info(f"正在处理第 {i}/{len(literatures)} 个文学作品: {liter_name}")
            if process_literature_tokens(liter_name):
                success_count += 1
                logger.info(f"文学作品 {liter_name} 处理成功")
            else:
                logger.error(f"文学作品 {liter_name} 处理失败")
        
        # 输出总结
        logger.info(f"处理完成！成功: {success_count}, 失败: {len(literatures)-success_count}")
        
    except Exception as e:
        logger.error(f"获取文学作品列表时出错: {str(e)}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()