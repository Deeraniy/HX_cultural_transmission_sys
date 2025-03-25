import os
import pymysql

def merge_sentiment_files(folder_path, output_file):
    """合并文件夹下所有txt文件的内容到一个文件"""
    words = set()
    encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'big5', 'latin1']
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            for encoding in encodings:
                try:
                    with open(os.path.join(folder_path, filename), 'r', encoding=encoding) as f:
                        words.update(line.strip() for line in f if line.strip())
                    print(f"成功使用 {encoding} 读取文件 {filename}")
                    break
                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    print(f"读取文件 {filename} 时发生错误: {str(e)}")
                    break
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for word in sorted(words):
            f.write(word + '\n')
    return words

def load_sensitive_words(file_path='app01/filter_for_comments/sensitive_words_lines.txt'):
    """加载敏感词"""
    encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'big5', 'latin1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                words = {line.strip() for line in f if line.strip()}
            print(f"成功使用 {encoding} 读取敏感词文件")
            return words
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"读取敏感词文件时发生错误: {str(e)}")
            return set()
    
    print("无法使用任何编码读取敏感词文件")
    return set()

def process_tokens():
    # 设置正确的路径
    base_path = 'app01/sentiments_on_tokens'
    positive_path = os.path.join(base_path, 'positive')
    negative_path = os.path.join(base_path, 'negative')
    
    # 连接数据库
    conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', 
                          passwd='song', db='hx_cultural_transmission_sys', 
                          charset='utf8')
    cursor = conn.cursor()
    
    try:
        # 合并情感词文件
        positive_words = merge_sentiment_files(positive_path, os.path.join(base_path, 'positive.txt'))
        negative_words = merge_sentiment_files(negative_path, os.path.join(base_path, 'negative.txt'))
        sensitive_words = load_sensitive_words()
        
        print(f"加载了 {len(positive_words)} 个positive词")
        print(f"加载了 {len(negative_words)} 个negative词")
        print(f"加载了 {len(sensitive_words)} 个敏感词")
        
        # 处理每个token表
        tables = ['spot_token', 'liter_token', 'food_token', 'folk_token']
        
        for table in tables:
            print(f"\n处理表 {table}:")
            
            # 清空sentiment值
            cursor.execute(f"UPDATE {table} SET sentiment = NULL")
            
            # 删除敏感词
            placeholders = ', '.join(['%s'] * len(sensitive_words))
            if sensitive_words:
                cursor.execute(f"""
                    DELETE FROM {table} 
                    WHERE token_name IN ({placeholders})
                """, list(sensitive_words))
                print(f"删除了 {cursor.rowcount} 个敏感词")
            
            # 更新情感值
            # 先处理positive
            placeholders = ', '.join(['%s'] * len(positive_words))
            if positive_words:
                cursor.execute(f"""
                    UPDATE {table} 
                    SET sentiment = 'positive' 
                    WHERE token_name IN ({placeholders})
                """, list(positive_words))
                print(f"更新了 {cursor.rowcount} 个positive词")
            
            # 再处理negative
            placeholders = ', '.join(['%s'] * len(negative_words))
            if negative_words:
                cursor.execute(f"""
                    UPDATE {table} 
                    SET sentiment = 'negative' 
                    WHERE token_name IN ({placeholders})
                """, list(negative_words))
                print(f"更新了 {cursor.rowcount} 个negative词")
            
            # 剩余的设为neutral
            cursor.execute(f"""
                UPDATE {table} 
                SET sentiment = 'neutral' 
                WHERE sentiment IS NULL
            """)
            print(f"更新了 {cursor.rowcount} 个neutral词")
            
            conn.commit()
            
        print("\n处理完成")
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
        conn.rollback()
    
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    process_tokens()
