import pymysql
from deep_translator import GoogleTranslator
import re
import emoji

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
    
    # 1. 首先保护所有**包围的内容
    asterisk_pattern = r'(\*\*.*?\*\*)'
    asterisk_matches = re.finditer(asterisk_pattern, text)
    for match in asterisk_matches:
        protected_items.append(match.group())
        
    # 2. 使用emoji库识别和保护所有表情符号
    emoji_pattern = emoji.get_emoji_regexp()
    emoji_matches = emoji_pattern.finditer(text)
    for match in emoji_matches:
        protected_items.append(match.group())
    
    # 3. 保护其他特殊Unicode字符（比如箭头、特殊符号等）
    special_chars_pattern = r'([^\w\s\u4e00-\u9fff.,?!，。？！、])'
    special_matches = re.finditer(special_chars_pattern, text)
    for match in special_matches:
        if match.group() not in protected_items:  # 避免重复添加已保护的内容
            protected_items.append(match.group())
    
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
        
        for row in rows:
            report_id, content = row
            
            try:
                # 提取需要保护的内容
                protected_items, clean_text = extract_format_symbols(content)
                
                # 翻译清理后的文本
                translated = translator.translate(clean_text)
                
                # 还原被保护的内容
                final_translation = restore_format_symbols(translated, protected_items)
                
                # 更新数据库
                cursor.execute(
                    "UPDATE report SET en_content = %s WHERE report_id = %s",
                    (final_translation, report_id)
                )
                conn.commit()
                print(f"已翻译 report_id: {report_id}")
                
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
