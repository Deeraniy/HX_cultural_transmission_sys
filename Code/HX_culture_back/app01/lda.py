import numpy as np
import pandas as pd
import jieba
import re
import pymysql
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# 配置日志
logger = logging.getLogger(__name__)

def top_words_data_frame(model: LatentDirichletAllocation,
                        tf_idf_vectorizer: TfidfVectorizer,
                        n_top_words: int) -> pd.DataFrame:
    """获取每个主题的前N个主题词"""
    rows = []
    feature_names = tf_idf_vectorizer.get_feature_names_out()
    for topic in model.components_:
        top_words = [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
        rows.append(top_words)
    return pd.DataFrame(rows)

def process_comments_lda(comments, n_topics=5, n_top_words=5):
    """处理评论并返回LDA结果"""
    # 设置停用词
    stop_words_set = set(['你', '我'])
    pattern = '[\\s\\d,.<>/?:;\'\"[\\]{}()\\|~!\t"@#$%^&*\\-_=+，。\n《》、？：；""''｛｝【】（）…￥！—┄－]+'
    
    # 准备数据
    df = pd.DataFrame({'text': comments}).drop_duplicates()
    
    # 文本预处理：去重、去缺失、分词
    df['cut'] = (
        df['text']
        .apply(lambda x: str(x))
        .apply(lambda x: re.sub(pattern, ' ', x))
        .apply(lambda x: " ".join([word for word in jieba.lcut(x) if word not in stop_words_set]))
    )
    
    # 构造 tf-idf
    tf_idf_vectorizer = TfidfVectorizer()
    tf_idf = tf_idf_vectorizer.fit_transform(df['cut'])
    
    # LDA 模型
    lda = LatentDirichletAllocation(
        n_components=n_topics,
        max_iter=50,
        learning_method='online',
        learning_offset=50,
        random_state=0
    )
    
    # 训练 LDA 模型
    lda.fit(tf_idf)
    
    # 获取主题词
    return top_words_data_frame(lda, tf_idf_vectorizer, n_top_words)

def process_all_topics():
    """处理所有类型的评论并存储主题"""
    conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', 
                          passwd='song', db='hx_cultural_transmission_sys', 
                          charset='utf8')
    cursor = conn.cursor()
    
    try:
        # 定义要处理的表和对应的主题表
        tables = [
            ('user_comment_spot', 'spot_topic', 'spot_id', 'spot'),
            ('user_comment_literature', 'liter_topic', 'liter_id', 'literature'),
            ('user_comment_food', 'food_topic', 'food_id', 'food'),
            ('user_comment_folk', 'folk_topic', 'folk_id', 'folk')
        ]
        
        for comment_table, topic_table, id_field, ref_table in tables:
            print(f"\n处理 {comment_table} 表...")
            
            # 清空对应的主题表
            print(f"清空 {topic_table} 表...")
            cursor.execute(f"TRUNCATE TABLE {topic_table}")
            conn.commit()
            
            # 获取所有不同的ID，直接从原始表获取
            cursor.execute(f"SELECT DISTINCT {id_field} FROM {ref_table}")
            all_ids = cursor.fetchall()
            print(f"找到 {len(all_ids)} 个{ref_table}")
            
            # 为每个表重置 topic_id 计数
            topic_id_counter = 1
            
            # 对每个ID进行处理
            for (item_id,) in all_ids:
                # 获取该ID的所有评论
                cursor.execute(f"""
                    SELECT comment_text 
                    FROM {comment_table} 
                    WHERE {id_field} = %s
                """, [item_id])
                comments = cursor.fetchall()
                
                if not comments:
                    print(f"跳过 {ref_table} ID: {item_id} (无评论)")
                    continue
                
                # 提取评论文本
                comment_texts = [c[0] for c in comments]
                
                # LDA处理
                topic_words_df = process_comments_lda(comment_texts)
                
                # 存储主题词
                for topic_idx, topic_words in enumerate(topic_words_df.values, 1):
                    for word_idx, word in enumerate(topic_words, 1):
                        cursor.execute(f"""
                            INSERT INTO {topic_table} 
                            (topic_id, topic_word, {id_field}, area)
                            VALUES (%s, %s, %s, %s)
                        """, [topic_id_counter, word, item_id, word_idx])
                        topic_id_counter += 1
                
                conn.commit()
                print(f"已处理 {ref_table} ID: {item_id}, 生成 {len(topic_words_df.values) * 5} 个主题词")
            
        print("\n所有主题处理完成")
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
        conn.rollback()
    
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    process_all_topics()
