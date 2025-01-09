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
    """
    过滤词语
    word: 待过滤的词
    min_length: 最小词长度
    """
    # 读取停用词
    with open("stopwords.txt", 'r', encoding='utf-8') as f:
        stopwords = set([line.strip() for line in f])
    
    # 过滤条件：长度大于等于min_length且不在停用词中
    return len(word) >= min_length and word not in stopwords

def process_liter_tokens(liter_name):
    """处理文学评论分词并更新数据库"""
    try:
        if not liter_name:
            logger.error("文学作品名称不能为空")
            return False

        # 获取liter_id的连接
        conn = get_db_connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 获取liter_id
        liter_sql = "SELECT liter_id FROM literature WHERE liter_name = %s"
        cursor.execute(liter_sql, (liter_name,))
        liter_result = cursor.fetchone()
        
        if not liter_result:
            logger.error(f'未找到文学作品: {liter_name}')
            cursor.close()
            conn.close()
            return False
        
        liter_id = liter_result['liter_id']
        
        # 检查是否已有足够的分词
        token_count = check_token_count(liter_id)
        if token_count >= 500:
            logger.info(f"文学作品 {liter_name} (ID: {liter_id}) 已有 {token_count} 个分词，跳过处理")
            cursor.close()
            conn.close()
            return True
            
        logger.info(f"处理文学作品: {liter_name} (ID: {liter_id})")

        # 获取评论的连接
        conn = get_db_connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 修改SQL查询，包含comment_id
        comment_sql = "SELECT comment_id, comment_text FROM user_comment_literature WHERE liter_id = %s"
        cursor.execute(comment_sql, (liter_id,))
        comments = cursor.fetchall()
        
        cursor.close()
        conn.close()

        # 每100条评论提交一次事务
        batch_size = 100
        total_words = 0
        word_batch = []
        comment_ids = []  # 存储对应的comment_id

        # 先收集所有词语
        for comment in comments:
            words = jieba.cut(comment['comment_text'])
            filtered_words = [word for word in words if filter_words(word)]
            
            if len(filtered_words) > 10:
                filtered_words = random.sample(filtered_words, 10)
            
            # 为每个词语添加对应的comment_id
            word_batch.extend([(word, comment['comment_id']) for word in filtered_words])
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
    """获取数据库连接，带有重试机制"""
    max_retries = 3
    base_delay = 5  # 基础等待时间（秒）
    
    for attempt in range(max_retries):
        try:
            return pymysql.connect(
                host='120.233.26.237', 
                port=15320, 
                user='root', 
                passwd='kissme77', 
                db='hx_cultural_transmission_sys', 
                charset='utf8',
                connect_timeout=30,    # 增加连接超时时间
                read_timeout=30,
                write_timeout=30
            )
        except pymysql.Error as e:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt) * (1 + random.random())
                logger.warning(f"数据库连接失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}\n等待 {delay:.1f} 秒后重试...")
                time.sleep(delay)
            else:
                logger.error(f"数据库连接失败，已达到最大重试次数: {str(e)}")
                raise

def process_word_batch(words, liter_id):
    """处理一批词语，带有重试机制"""
    max_retries = 5  # 最大重试次数
    base_delay = 60  # 基础等待时间（秒）
    
    for word, comment_id in words:
        retry_count = 0
        while retry_count < max_retries:
            try:
                conn = get_db_connection()
                cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
                
                # 检查词语是否存在
                check_sql = """
                    SELECT token_id, count 
                    FROM liter_token 
                    WHERE token_name = %s AND liter_id = %s AND comment_id = %s
                """
                cursor.execute(check_sql, (word, liter_id, comment_id))
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
                        INSERT INTO liter_token (token_name, count, liter_id, comment_id) 
                        VALUES (%s, 1, %s, %s)
                    """
                    cursor.execute(insert_sql, (word, liter_id, comment_id))
                    
                conn.commit()
                logger.debug(f"成功处理词语: {word} (评论ID: {comment_id})")
                break  # 成功处理，跳出重试循环
                
            except pymysql.Error as e:
                retry_count += 1
                if retry_count < max_retries:
                    delay = base_delay * (1 + random.random())  # 添加随机延迟
                    logger.warning(
                        f"处理词语 {word} (评论ID: {comment_id}) 时出错 "
                        f"(尝试 {retry_count}/{max_retries}): {str(e)}\n"
                        f"等待 {delay:.1f} 秒后重试..."
                    )
                    time.sleep(delay)
                    if 'conn' in locals():
                        try:
                            conn.rollback()
                        except:
                            pass
                else:
                    logger.error(
                        f"处理词语 {word} (评论ID: {comment_id}) 失败，"
                        f"已达到最大重试次数 ({max_retries}): {str(e)}"
                    )
            except Exception as e:
                logger.error(f"处理词语 {word} (评论ID: {comment_id}) 时出现未知错误: {str(e)}")
                break  # 非数据库错误直接跳过
            finally:
                if 'cursor' in locals():
                    try:
                        cursor.close()
                    except:
                        pass
                if 'conn' in locals():
                    try:
                        conn.close()
                    except:
                        pass

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

        # 修改查询，包含comment_id
        frequency_sql = """
            SELECT token_name as word, count as frequency, sentiment, comment_id
            FROM liter_token 
            WHERE liter_id = %s 
            ORDER BY count DESC 
            LIMIT 30 OFFSET 20
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

def retry_with_backoff(func, *args, max_retries=3, initial_delay=1):
    """带有指数退避的重试机制"""
    for attempt in range(max_retries):
        try:
            return func(*args)
        except Exception as e:
            delay = initial_delay * (2 ** attempt)  # 指数退避
            logger.warning(f"第 {attempt + 1} 次尝试失败: {str(e)}, {delay} 秒后重试...")
            time.sleep(delay)
            if attempt == max_retries - 1:  # 最后一次尝试
                raise e
    return False

def check_token_count(liter_id):
    """检查文学作品的token数量"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM liter_token WHERE liter_id = %s", (liter_id,))
        count = cursor.fetchone()[0]
        return count
    finally:
        cursor.close()
        conn.close()

def get_insufficient_liters():
    """获取token数量不足的文学作品"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        
        # 获取所有文学作品的token数量
        sql = """
            SELECT l.liter_id, l.liter_name, COUNT(t.token_id) as token_count
            FROM literature l
            LEFT JOIN liter_token t ON l.liter_id = t.liter_id
            GROUP BY l.liter_id, l.liter_name
            HAVING token_count < 500 OR token_count IS NULL
        """
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def clean_existing_tokens(liter_id):
    """清理现有的tokens"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM liter_token WHERE liter_id = %s", (liter_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    try:
        # 连接数据库获取所有文学作品
        conn = get_db_connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        
        # 获取所有文学作品
        liters_sql = "SELECT liter_name FROM literature"
        cursor.execute(liters_sql)
        liters = [row['liter_name'] for row in cursor.fetchall()]
        
        logger.info(f"共找到 {len(liters)} 个文学作品待处理")
        
        # 处理每个文学作品
        success_count = 0
        skipped_count = 0  # 记录跳过的数量
        failed_liters = []
        
        for i, liter_name in enumerate(liters, 1):
            logger.info(f"正在处理第 {i}/{len(liters)} 个文学作品: {liter_name}")
            try:
                # 检查是否已有足够的分词
                liter_id = get_liter_id(liter_name)
                if liter_id and check_token_count(liter_id) >= 500:
                    logger.info(f"文学作品 {liter_name} 已有足够分词，跳过处理")
                    skipped_count += 1
                    continue
                
                # 使用重试机制处理文学作品
                if retry_with_backoff(process_liter_tokens, liter_name, max_retries=3):
                    success_count += 1
                    logger.info(f"文学作品 {liter_name} 处理成功")
                else:
                    failed_liters.append(liter_name)
                    logger.error(f"文学作品 {liter_name} 处理失败")
            except Exception as e:
                failed_liters.append(liter_name)
                logger.error(f"处理文学作品 {liter_name} 时出错: {str(e)}")
        
        # 输出首次处理的总结
        logger.info(f"""
        首次处理完成！
        跳过: {skipped_count}
        成功: {success_count}
        失败: {len(failed_liters)}
        """)
        
        # 获取token数量不足的文学作品
        insufficient_liters = get_insufficient_liters()
        logger.info(f"发现 {len(insufficient_liters)} 个token数量不足的文学作品")
        
        # 重新处理token数量不足的文学作品
        reprocess_success = 0
        for liter in insufficient_liters:
            logger.info(f"重新处理token不足的文学作品: {liter['liter_name']} (当前token数: {liter['token_count']})")
            try:
                # 清理现有的tokens
                clean_existing_tokens(liter['liter_id'])
                
                # 重新处理
                if retry_with_backoff(process_liter_tokens, liter['liter_name'], max_retries=5):
                    reprocess_success += 1
                    logger.info(f"文学作品 {liter['liter_name']} 重新处理成功")
                else:
                    logger.error(f"文学作品 {liter['liter_name']} 重新处理失败")
            except Exception as e:
                logger.error(f"重新处理文学作品 {liter['liter_name']} 时出错: {str(e)}")
        
        # 最终总结
        logger.info(f"""
        处理完成！
        首次处理:
            - 跳过: {skipped_count}
            - 成功: {success_count}
            - 失败: {len(failed_liters)}
        重新处理:
            - 成功: {reprocess_success}
            - 失败: {len(insufficient_liters) - reprocess_success}
        """)
        
        # 输出最终仍然token不足的文学作品
        final_insufficient = get_insufficient_liters()
        if final_insufficient:
            logger.warning("以下文学作品的token数量仍然不足:")
            for liter in final_insufficient:
                logger.warning(f"- {liter['liter_name']}: {liter['token_count']} tokens")
        
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close() 