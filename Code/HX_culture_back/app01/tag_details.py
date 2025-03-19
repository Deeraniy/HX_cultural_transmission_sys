from django.http import JsonResponse
import pymysql

def get_tag_details(request):
    if request.method == 'GET':
        tag_ids = request.GET.get('tag_ids')
        print("\n=== 开始处理标签详情请求 ===")
        print(f"接收到的tag_ids: {tag_ids}")
        
        if not tag_ids:
            print("错误：未提供标签ID")
            return JsonResponse({"error": "未提供标签ID"})
            
        tag_id_list = tag_ids.split(',')
        print(f"处理后的tag_id列表: {tag_id_list}")
        
        conn = pymysql.connect(host='60.215.128.117', port=15320, user='root', passwd='kissme77',
                               db='hx_cultural_transmission_sys', charset='utf8')
        cursor = conn.cursor()
        
        try:
            detailed_tags = []
            
            # 首先获取标签基本信息
            for tag_id in tag_id_list:
                print(f"\n处理标签ID: {tag_id}")
                sql_tag = """
                SELECT tag_id, tag_name, theme_name, origin_id
                FROM tag 
                WHERE tag_id = %s
                """
                cursor.execute(sql_tag, (tag_id,))
                tag_info = cursor.fetchone()
                
                if tag_info:
                    tag_id, tag_name, theme_name, origin_id = tag_info
                    print(f"找到标签: {tag_name}, 主题: {theme_name}, 原始ID: {origin_id}")
                    
                    # 根据theme_name确定要查询的表和ID字段名
                    theme_table_map = {
                        'folk': ('folk', 'folk_id'),
                        'food': ('food', 'food_id'),
                        'literature': ('literature', 'liter_id'),
                        'spot': ('spot', 'spot_id'),
                        'history': ('history', 'history_id')
                    }
                    
                    table_info = theme_table_map.get(theme_name.lower())
                    if table_info:
                        table_name, id_column = table_info
                        print(f"查询表: {table_name}, ID列: {id_column}")
                        
                        detail_sql = f"""
                        SELECT *
                        FROM {table_name}
                        WHERE {id_column} = %s
                        """
                        cursor.execute(detail_sql, (origin_id,))
                        detail_info = cursor.fetchone()
                        
                        if detail_info:
                            print("找到详细信息")
                            # 获取列名
                            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                            columns = [column[0] for column in cursor.fetchall()]
                            detail_dict = dict(zip(columns, detail_info))
                            
                            # 组合信息
                            tag_detail = {
                                'tag_id': tag_id,
                                'tag_name': tag_name,
                                'theme_name': theme_name,
                                'origin_id': origin_id,
                                'details': detail_dict,
                                'image_url': detail_dict.get('image_url') or detail_dict.get('image') or '',
                                'description': detail_dict.get('description') or detail_dict.get('desc') or '',
                                'title': detail_dict.get('name') or detail_dict.get('title') or tag_name
                            }
                            print(f"处理完成的标签详情: {tag_detail}")
                            detailed_tags.append(tag_detail)
                        else:
                            print(f"未找到ID为 {origin_id} 的详细信息")
                    else:
                        print(f"未知的主题类型: {theme_name}")
                else:
                    print(f"未找到标签ID: {tag_id}")
            
            print(f"\n=== 处理完成 ===")
            print(f"总共处理了 {len(detailed_tags)} 个标签")
            return JsonResponse({
                'status': 'success',
                'tag_details': detailed_tags
            })
            
        except Exception as e:
            print(f"发生错误: {str(e)}")
            conn.rollback()
            return JsonResponse({
                'status': 'error',
                'message': f'获取标签详细信息失败: {str(e)}'
            })
        finally:
            cursor.close()
            conn.close()
            print("数据库连接已关闭")
    else:
        print("收到非GET请求")
        return JsonResponse({
            'status': 'error',
            'message': '不是GET请求'
        }) 