import pymysql
from deep_translator import GoogleTranslator
import re
import emoji
import time

def get_db_connection():
    """获取数据库连接"""
    return pymysql.connect(
        host='8.148.26.99',
        port=3306,
        user='root',
        passwd='song',
        db='hx_cultural_transmission_sys',
        charset='utf8',
        connect_timeout=10,
        read_timeout=30,
        write_timeout=30
    )

def extract_format_symbols(text):
    """提取文本中的格式符号和表情"""
    # 存储所有需要保护的特殊内容
    protected_items = []
    
    # 1. 保护所有**包围的年份和月份
    year_month_pattern = r'(\*\*\d{4}年\d{1,2}月：\*\*)'
    year_month_matches = re.finditer(year_month_pattern, text)
    for match in year_month_matches:
        protected_items.append(match.group())

    # 2. 保护所有数字和百分比
    number_pattern = r'(\d+\.?\d*%?)'
    number_matches = re.finditer(number_pattern, text)
    for match in number_matches:
        protected_items.append(match.group())
    
    # 3. 保护情感分布的括号内容
    distribution_pattern = r'(\(\d+\.?\d*%\))'
    distribution_matches = re.finditer(distribution_pattern, text)
    for match in distribution_matches:
        protected_items.append(match.group())
    
    # 4. 识别和保护所有表情符号
    for char in text:
        if emoji.is_emoji(char):
            if char not in protected_items:
                protected_items.append(char)
    
    # 5. 保护特定的标点符号和特殊字符
    special_chars = ['——', '、', '-', '&', '：', '**']
    for char in special_chars:
        if char in text:
            protected_items.append(char)
    
    # 替换所有需要保护的内容为占位符
    processed_text = text
    for i, item in enumerate(protected_items):
        processed_text = processed_text.replace(item, f'{{PLACEHOLDER_{i}}}', 1)
    
    return protected_items, processed_text

def restore_format_symbols(translated_text, protected_items):
    """还原格式符号和表情到翻译后的文本"""
    result = translated_text
    for i, item in enumerate(protected_items):
        result = result.replace(f'{{PLACEHOLDER_{i}}}', item, 1)
    return result

def translate_content():
    """将report表中的content翻译成英文并存入en_content"""
    conn = get_db_connection()
    cursor = conn.cursor()
    translator = GoogleTranslator(source='zh-CN', target='en')

    try:
        # 获取所有需要翻译的内容
        cursor.execute("SELECT report_id, content FROM report WHERE en_content IS NULL OR en_content = ''")
        rows = cursor.fetchall()
        
        total_count = len(rows)
        print(f"总共需要翻译 {total_count} 条记录")
        
        for i, row in enumerate(rows, 1):
            report_id, content = row
            
            try:
                # 提取需要保护的内容
                protected_items, clean_text = extract_format_symbols(content)
                
                # 将长文本分段翻译，避免超出API限制
                segments = [clean_text[i:i+1000] for i in range(0, len(clean_text), 1000)]
                translated_segments = []
                
                for segment in segments:
                    # 添加重试机制
                    max_retries = 3
                    for attempt in range(max_retries):
                        try:
                            translated_segment = translator.translate(segment)
                            translated_segments.append(translated_segment)
                            # 成功翻译后等待一小段时间，避免请求过快
                            time.sleep(1)
                            break
                        except Exception as e:
                            if attempt == max_retries - 1:
                                raise e
                            time.sleep(2 ** attempt)  # 指数退避
                
                translated = ' '.join(translated_segments)
                
                # 还原被保护的内容
                final_translation = restore_format_symbols(translated, protected_items)
                
                # 更新数据库
                cursor.execute(
                    "UPDATE report SET en_content = %s WHERE report_id = %s",
                    (final_translation, report_id)
                )
                conn.commit()
                print(f"已翻译 {i}/{total_count}: report_id: {report_id}")
                
            except Exception as e:
                print(f"翻译失败 report_id: {report_id}, 错误: {str(e)}")
                continue
                
    except Exception as e:
        print(f"数据库操作失败: {str(e)}")
        
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    translate_content()
