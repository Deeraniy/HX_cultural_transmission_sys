from django.http import JsonResponse
import pymysql
from django.db import connection
from django.conf import settings
import time

def get_tag_details(request):
    if request.method == 'GET':
        start_time = time.time()
        tag_ids = request.GET.get('tag_ids')
        
        if not tag_ids:
            return JsonResponse({"error": "未提供标签ID"})
            
        tag_id_list = tag_ids.split(',')
        
        # 使用Django的数据库连接而不是直接使用pymysql
        with connection.cursor() as cursor:
            try:
                detailed_tags = []
                
                # 批量获取标签基本信息，而不是逐个查询
                placeholders = ', '.join(['%s'] * len(tag_id_list))
                sql_tag = f"""
                SELECT tag_id, tag_name, theme_name, origin_id
                FROM tag 
                WHERE tag_id IN ({placeholders})
                """
                cursor.execute(sql_tag, tag_id_list)
                tag_infos = cursor.fetchall()
                
                # 按主题分组标签，减少数据库查询次数
                tags_by_theme = {}
                for tag_info in tag_infos:
                    tag_id, tag_name, theme_name, origin_id = tag_info
                    theme_name = theme_name.lower() if theme_name else ''
                    
                    if theme_name not in tags_by_theme:
                        tags_by_theme[theme_name] = []
                    
                    tags_by_theme[theme_name].append({
                        'tag_id': tag_id,
                        'tag_name': tag_name,
                        'origin_id': origin_id
                    })
                
                # 主题表映射
                theme_table_map = {
                    'folk': ('folk', 'folk_id'),
                    'food': ('food', 'food_id'),
                    'literature': ('literature', 'liter_id'),
                    'spot': ('spot', 'spot_id'),
                    'history': ('history', 'history_id')
                }
                
                # 按主题批量查询详细信息
                for theme_name, tags in tags_by_theme.items():
                    if theme_name not in theme_table_map:
                        continue
                        
                    table_name, id_column = theme_table_map[theme_name]
                    
                    # 获取该主题下所有标签的原始ID
                    origin_ids = [tag['origin_id'] for tag in tags]
                    if not origin_ids:
                        continue
                    
                    # 批量查询详细信息
                    placeholders = ', '.join(['%s'] * len(origin_ids))
                    detail_sql = f"""
                    SELECT *
                    FROM {table_name}
                    WHERE {id_column} IN ({placeholders})
                    """
                    cursor.execute(detail_sql, origin_ids)
                    detail_infos = cursor.fetchall()
                    
                    # 获取列名
                    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                    columns = [column[0] for column in cursor.fetchall()]
                    
                    # 创建原始ID到详细信息的映射
                    detail_map = {}
                    for detail_info in detail_infos:
                        detail_dict = dict(zip(columns, detail_info))
                        origin_id = detail_dict.get(id_column)
                        if origin_id:
                            detail_map[origin_id] = detail_dict
                    
                    # 处理每个标签
                    for tag in tags:
                        origin_id = tag['origin_id']
                        detail_dict = detail_map.get(origin_id, {})
                        
                        # 特殊处理影视文学的描述
                        description = ''
                        if theme_name == 'literature':
                            description = detail_dict.get('text') or detail_dict.get('description') or ''
                        else:
                            description = detail_dict.get('description') or detail_dict.get('desc') or ''
                        
                        # 组合信息
                        tag_detail = {
                            'tag_id': tag['tag_id'],
                            'tag_name': tag['tag_name'],
                            'theme_name': theme_name,
                            'origin_id': origin_id,
                            'details': detail_dict,
                            'image_url': detail_dict.get('image_url') or detail_dict.get('image') or '',
                            'description': description,
                            'title': detail_dict.get('name') or detail_dict.get('title') or tag['tag_name']
                        }
                        detailed_tags.append(tag_detail)
                
                end_time = time.time()
                print(f"标签详情查询耗时: {end_time - start_time:.2f}秒")
                
                return JsonResponse({
                    'status': 'success',
                    'tag_details': detailed_tags
                })
                
            except Exception as e:
                print(f"发生错误: {str(e)}")
                return JsonResponse({
                    'status': 'error',
                    'message': f'获取标签详细信息失败: {str(e)}'
                })
    else:
        return JsonResponse({
            'status': 'error',
            'message': '不是GET请求'
        }) 