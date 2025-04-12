import pymysql
import json
import time

def export_culture_elements():
    start_time = time.time()
    result = []
    
    # 主题表映射
    theme_table_map = {
        'folk': ('folk', 'folk_id'),
        'food': ('food', 'food_id'),
        'literature': ('literature', 'liter_id'),
        'spot': ('spot', 'spot_id'),
    }
    
    try:
        # 连接数据库
        conn = pymysql.connect(
            host='8.148.26.99', 
            port=3306, 
            user='root', 
            passwd='song',
            db='hx_cultural_transmission_sys', 
            charset='utf8',
            connect_timeout=30
        )
        
        with conn.cursor() as cursor:
            # 遍历每个主题
            for theme_name, (table_name, id_column) in theme_table_map.items():
                # 获取该主题下的所有记录
                sql = f"""
                SELECT t.tag_name, t.theme_name, t.origin_id, d.*
                FROM tag t
                JOIN {table_name} d ON t.origin_id = d.{id_column}
                WHERE t.theme_name = %s
                """
                cursor.execute(sql, [theme_name])
                records = cursor.fetchall()
                
                # 获取列名
                cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                columns = [column[0] for column in cursor.fetchall()]
                
                # 处理每条记录
                for record in records:
                    tag_name = record[0]
                    theme_name = record[1]
                    origin_id = record[2]
                    detail_dict = dict(zip(columns, record[3:]))
                    
                    # 特殊处理影视文学的描述
                    description = ''
                    if theme_name == 'literature':
                        description = detail_dict.get('text') or detail_dict.get('description') or ''
                    else:
                        description = detail_dict.get('description') or detail_dict.get('desc') or ''
                    
                    # 获取标题
                    title = detail_dict.get('name') or detail_dict.get('title') or tag_name
                    
                    # 添加到结果列表
                    result.append({
                        'tag_id': origin_id,
                        'theme': theme_name,
                        'title': title,
                        'description': description
                    })
        
        # 将结果写入JSON文件
        with open('culture_elements.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        end_time = time.time()
        print(f"导出完成，共 {len(result)} 条记录")
        print(f"耗时: {end_time - start_time:.2f}秒")
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    export_culture_elements() 