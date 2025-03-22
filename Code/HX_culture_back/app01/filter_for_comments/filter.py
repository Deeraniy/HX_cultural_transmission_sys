import pymysql
from django.http import JsonResponse

def load_sensitive_words(file_path='./app01/filter_for_comments/sensitive_words_lines.txt'):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return {line.strip() for line in file if line.strip()}
    except FileNotFoundError:
        print("警告：未找到敏感词文件，将不进行敏感词过滤")
        return set()

def filter_positive_comments():
    conn = pymysql.connect(host='60.215.128.117', port=15320, user='root', 
                          passwd='kissme77', db='hx_cultural_transmission_sys', 
                          charset='utf8')
    cursor = conn.cursor()
    
    try:
        # 先清空filtered_user_comment表
        print("清空filtered_user_comment表...")
        cursor.execute("TRUNCATE TABLE filtered_user_comment")
        conn.commit()
        
        # 统一处理所有表
        for table in ['user_comment_folk', 'user_comment_food', 
                     'user_comment_literature', 'user_comment_spot']:
            print(f"\n处理表: {table}")
            category = table.split('_')[-1]
            
            # 特殊处理 literature 的字段名
            id_field = 'liter_id' if category == 'literature' else f'{category}_id'
            
            insert_query = f"""
            INSERT INTO filtered_user_comment 
            (user_id, comment_text, comment_time, ip_location, 
             like_count, tag_id, sentiment, sentiment_confidence, platform, checked)
            SELECT 
                c.user_id,
                c.comment_text,
                c.comment_time,
                c.ip_location,
                c.like_count,
                t.tag_id,
                c.sentiment,
                c.sentiment_confidence,
                c.platform,
                0 as checked
            FROM {table} c
            JOIN tag t ON t.origin_id = c.{id_field}
                AND t.theme_name = '{category}'
            WHERE c.sentiment = 'positive'
            """
            cursor.execute(insert_query)
            print(f"插入了 {cursor.rowcount} 条记录")
            conn.commit()

        print("\n数据过滤完成")

    except Exception as e:
        print(f"发生错误: {str(e)}")
        conn.rollback()
    
    finally:
        cursor.close()
        conn.close()

def get_filtered_comments_by_tag(request):
    if request.method == 'GET':
        tag_name = request.GET.get('name')
        if not tag_name:
            return JsonResponse({'error': '请提供tag_name参数'}, status=400)
            
        conn = pymysql.connect(host='60.215.128.117', port=15320, user='root', 
                             passwd='kissme77', db='hx_cultural_transmission_sys', 
                             charset='utf8')
        cursor = conn.cursor(pymysql.cursors.DictCursor)  # 使用字典游标
        
        try:
            # 先根据tag_name获取tag_id
            cursor.execute("SELECT tag_id FROM tag WHERE tag_name = %s", [tag_name])
            tag_result = cursor.fetchone()
            
            if not tag_result:
                return JsonResponse({'error': '未找到对应的标签'}, status=404)
                
            tag_id = tag_result['tag_id']
            
            # 获取该tag_id的所有评论
            cursor.execute("""
                SELECT * FROM filtered_user_comment 
                WHERE tag_id = %s
                ORDER BY comment_time DESC
            """, [tag_id])
            
            comments = cursor.fetchall()
            
            return JsonResponse({
                'tag_name': tag_name,
                'tag_id': tag_id,
                'total_count': len(comments),
                'comments': comments
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
        finally:
            cursor.close()
            conn.close()
            
    return JsonResponse({'error': '仅支持GET请求'}, status=405)

if __name__ == "__main__":
    filter_positive_comments()
