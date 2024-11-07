import jieba
import pymysql
import logging

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

def process_spot_tokens(spot_name):
    """处理景点评论分词并更新数据库"""
    try:
        if not spot_name:
            logger.error("景点名称不能为空")
            return False

        # 数据库连接
        conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', 
                             passwd='kissme77', db='hx_cultural_transmission_sys', 
                             charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 获取spot_id
        spot_sql = "SELECT spot_id FROM scenicspot WHERE spot_name = %s"
        cursor.execute(spot_sql, (spot_name,))
        spot_result = cursor.fetchone()
        
        if not spot_result:
            logger.error(f'未找到景点: {spot_name}')
            return False
        
        spot_id = spot_result['spot_id']
        logger.info(f"处理景点: {spot_name} (ID: {spot_id})")

        # 获取所有评论
        comment_sql = "SELECT content FROM usercomment WHERE spot_id = %s"
        cursor.execute(comment_sql, (spot_id,))
        comments = cursor.fetchall()

        # 处理每条评论
        total_words = 0
        for comment in comments:
            # 分词
            words = jieba.cut(comment['content'])
            
            # 过滤词语
            filtered_words = [word for word in words if filter_words(word)]
            
            # 更新数据库
            for word in filtered_words:
                total_words += 1
                # 检查词语是否存在
                check_sql = """
                    SELECT token_id, count 
                    FROM token 
                    WHERE token_name = %s AND spot_id = %s
                """
                cursor.execute(check_sql, (word, spot_id))
                token_result = cursor.fetchone()
                
                if token_result:
                    # 更新计数
                    update_sql = """
                        UPDATE token 
                        SET count = count + 1 
                        WHERE token_id = %s
                    """
                    cursor.execute(update_sql, (token_result['token_id'],))
                else:
                    # 插入新词
                    insert_sql = """
                        INSERT INTO token (token_name, count, spot_id) 
                        VALUES (%s, 1, %s)
                    """
                    cursor.execute(insert_sql, (word, spot_id))
                    logger.info(f"插入新词: {word}")

        conn.commit()
        logger.info(f"处理完成，共处理 {len(comments)} 条评论，{total_words} 个词语")
        return True

    except Exception as e:
        logger.error(f"处理分词时出错: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    try:
        # 连接数据库获取所有景点
        conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', 
                             passwd='kissme77', db='hx_cultural_transmission_sys', 
                             charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        
        # 获取所有景点
        spots_sql = "SELECT spot_name FROM scenicspot"
        cursor.execute(spots_sql)
        spots = [row['spot_name'] for row in cursor.fetchall()]
        
        logger.info(f"共找到 {len(spots)} 个景点待处理")
        
        # 处理每个景点
        success_count = 0
        for i, spot_name in enumerate(spots, 1):
            logger.info(f"正在处理第 {i}/{len(spots)} 个景点: {spot_name}")
            if process_spot_tokens(spot_name):
                success_count += 1
                logger.info(f"景点 {spot_name} 处理成功")
            else:
                logger.error(f"景点 {spot_name} 处理失败")
        
        # 输出总结
        logger.info(f"处理完成！成功: {success_count}, 失败: {len(spots)-success_count}")
        
    except Exception as e:
        logger.error(f"获取景点列表时出错: {str(e)}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()