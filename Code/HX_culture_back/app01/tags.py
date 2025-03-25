from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import pymysql
import json

def get_db_connection():
    return pymysql.connect(
        host='8.148.26.99',
        port=3306,
        user='root',
        passwd='song',
        db='hx_cultural_transmission_sys',
        charset='utf8'
    )

@require_http_methods(["GET"])
def get_all_tags(request):
    """
    获取所有标签
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        sql = """
        SELECT tag_id, tag_name, theme_name, total_clicks, total_likes
        FROM tag
        """
        cursor.execute(sql)
        tags = cursor.fetchall()
        
        result = [{
            'id': tag[0],
            'tag_name': tag[1],
            'theme_name': tag[2],
            'total_clicks': tag[3],
            'total_likes': tag[4]
        } for tag in tags]
        
        return JsonResponse({'code': 200, 'data': result})
    except Exception as e:
        return JsonResponse({'code': 500, 'message': str(e)})
    finally:
        cursor.close()
        conn.close()

@require_http_methods(["POST"])
def view_tag(request):
    """
    记录用户浏览标签
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        tag_id = data.get('tag_id')
        
        print(f"记录浏览: user_id={user_id}, tag_id={tag_id}")
        
        # 确保 total_clicks 不为 NULL
        cursor.execute("""
            UPDATE tag 
            SET total_clicks = COALESCE(total_clicks, 0)
            WHERE tag_id = %s
        """, (tag_id,))
        
        # 检查是否存在记录
        cursor.execute("""
            SELECT click_count FROM tag_user 
            WHERE user_id = %s AND tag_id = %s
        """, (user_id, tag_id))
        tag_user = cursor.fetchone()
        
        if tag_user:
            # 更新点击次数
            cursor.execute("""
                UPDATE tag_user 
                SET click_count = click_count + 1 
                WHERE user_id = %s AND tag_id = %s
            """, (user_id, tag_id))
        else:
            # 创建新记录
            cursor.execute("""
                INSERT INTO tag_user (user_id, tag_id, click_count, is_favorite, is_liked) 
                VALUES (%s, %s, 1, 0, 0)
            """, (user_id, tag_id))
        
        # 更新标签总点击量
        cursor.execute("""
            UPDATE tag 
            SET total_clicks = total_clicks + 1 
            WHERE tag_id = %s
        """, (tag_id,))
        
        # 获取更新后的点击量
        cursor.execute("""
            SELECT COALESCE(total_clicks, 0) as total_clicks
            FROM tag 
            WHERE tag_id = %s
        """, (tag_id,))
        total_clicks = cursor.fetchone()[0]
        print(f"更新后的点击量: {total_clicks}")
        
        conn.commit()
        return JsonResponse({
            'code': 200, 
            'message': '浏览记录已更新',
            'data': {
                'total_clicks': total_clicks
            }
        })
    except Exception as e:
        print(f"记录浏览出错: {str(e)}")
        conn.rollback()
        return JsonResponse({'code': 500, 'message': str(e)})
    finally:
        cursor.close()
        conn.close()

@require_http_methods(["POST"])
def toggle_like(request):
    """
    切换标签点赞状态
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        tag_id = data.get('tag_id')
        
        print(f"接收到点赞请求: user_id={user_id}, tag_id={tag_id}")
        
        # 检查当前点赞状态
        cursor.execute("""
            SELECT is_liked FROM tag_user 
            WHERE user_id = %s AND tag_id = %s
        """, (user_id, tag_id))
        
        result = cursor.fetchone()
        is_liked = result[0] if result else False
        
        print(f"当前点赞状态: {is_liked}")
        
        # 切换点赞状态
        new_is_liked = not is_liked
        
        # 更新 tag_user 表
        if result:
            cursor.execute("""
                UPDATE tag_user 
                SET is_liked = %s
                WHERE user_id = %s AND tag_id = %s
            """, (new_is_liked, user_id, tag_id))
        else:
            cursor.execute("""
                INSERT INTO tag_user (user_id, tag_id, is_liked, is_favorite, click_count)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, tag_id, new_is_liked, False, 1))
        
        # 先确保 total_likes 不为 NULL
        cursor.execute("""
            UPDATE tag 
            SET total_likes = COALESCE(total_likes, 0)
            WHERE tag_id = %s
        """, (tag_id,))
        
        # 更新 tag 表中的总点赞数
        if new_is_liked:
            cursor.execute("""
                UPDATE tag 
                SET total_likes = total_likes + 1
                WHERE tag_id = %s
            """, (tag_id,))
        else:
            cursor.execute("""
                UPDATE tag 
                SET total_likes = GREATEST(total_likes - 1, 0)
                WHERE tag_id = %s
            """, (tag_id,))
        
        # 获取更新后的总点赞数
        cursor.execute("""
            SELECT COALESCE(total_likes, 0) as total_likes
            FROM tag 
            WHERE tag_id = %s
        """, (tag_id,))
        total_likes = cursor.fetchone()[0]
        
        print(f"更新后的点赞状态: {new_is_liked}, 总点赞数: {total_likes}")
        
        conn.commit()
        
        return JsonResponse({
            'code': 200, 
            'data': {
                'is_liked': new_is_liked,
                'total_likes': total_likes
            }
        })
    except Exception as e:
        print(f"点赞操作出错: {str(e)}")
        conn.rollback()
        return JsonResponse({'code': 500, 'message': str(e)})
    finally:
        cursor.close()
        conn.close()

@require_http_methods(["POST"])
def toggle_favorite(request):
    """
    切换标签收藏状态
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        tag_id = data.get('tag_id')
        
        # 获取当前收藏状态
        cursor.execute("""
            SELECT is_favorite FROM tag_user 
            WHERE user_id = %s AND tag_id = %s
        """, (user_id, tag_id))
        result = cursor.fetchone()
        
        if result:
            new_status = not result[0]
            cursor.execute("""
                UPDATE tag_user 
                SET is_favorite = %s 
                WHERE user_id = %s AND tag_id = %s
            """, (new_status, user_id, tag_id))
        else:
            cursor.execute("""
                INSERT INTO tag_user (user_id, tag_id, click_count, is_favorite) 
                VALUES (%s, %s, 0, 1)
            """, (user_id, tag_id))
            new_status = True
        
        conn.commit()
        return JsonResponse({
            'code': 200,
            'message': '操作成功',
            'data': {
                'is_favorite': new_status
            }
        })
    except Exception as e:
        conn.rollback()
        return JsonResponse({'code': 500, 'message': str(e)})
    finally:
        cursor.close()
        conn.close()

@require_http_methods(["GET"])
def get_tag_status(request):
    """
    获取标签状态
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        user_id = request.GET.get('user_id')
        tag_id = request.GET.get('tag_id')
        
        print(f"获取标签状态: user_id={user_id}, tag_id={tag_id}")
        
        # 获取标签信息
        cursor.execute("""
            SELECT COALESCE(total_likes, 0) as total_likes, COALESCE(total_clicks, 0) as total_clicks
            FROM tag 
            WHERE tag_id = %s
        """, (tag_id,))
        
        tag_info = cursor.fetchone()
        
        if not tag_info:
            return JsonResponse({'code': 404, 'message': '标签不存在'})
        
        total_likes = tag_info[0]  # 已确保不为 NULL
        total_clicks = tag_info[1]
        
        print(f"标签信息: total_likes={total_likes}, total_clicks={total_clicks}")
        
        # 获取用户对该标签的状态
        cursor.execute("""
            SELECT is_liked, is_favorite, click_count 
            FROM tag_user 
            WHERE user_id = %s AND tag_id = %s
        """, (user_id, tag_id))
        
        user_tag = cursor.fetchone()
        
        is_liked = False
        is_favorite = False
        click_count = 0
        
        if user_tag:
            is_liked = bool(user_tag[0])
            is_favorite = bool(user_tag[1])
            click_count = user_tag[2] or 0
        
        print(f"用户标签状态: is_liked={is_liked}, is_favorite={is_favorite}, click_count={click_count}")
        
        return JsonResponse({
            'code': 200, 
            'data': {
                'total_likes': total_likes,
                'total_clicks': total_clicks,
                'is_liked': is_liked,
                'is_favorite': is_favorite,
                'click_count': click_count
            }
        })
    except Exception as e:
        print(f"获取标签状态出错: {str(e)}")
        return JsonResponse({'code': 500, 'message': str(e)})
    finally:
        cursor.close()
        conn.close()

@require_http_methods(["GET"])
def get_user_tag_status(request):
    """
    获取用户的所有标签状态
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        user_id = request.GET.get('user_id')
        print(f"获取用户 {user_id} 的标签状态")
        
        cursor.execute("""
            SELECT tag_id, is_favorite, click_count 
            FROM tag_user 
            WHERE user_id = %s
        """, (user_id,))
        tag_users = cursor.fetchall()
        print(f"找到 {len(tag_users)} 条用户标签记录")
        
        # 获取标签详细信息
        tag_ids = [tu[0] for tu in tag_users]
        if tag_ids:
            placeholders = ', '.join(['%s'] * len(tag_ids))
            cursor.execute(f"""
                SELECT tag_id, tag_name, theme_name, total_likes
                FROM tag
                WHERE tag_id IN ({placeholders})
            """, tag_ids)
            tags_info = {tag[0]: tag for tag in cursor.fetchall()}
        else:
            tags_info = {}
        
        result = [{
            'tag_id': tu[0],
            'tag_name': tags_info.get(tu[0], [None, '未知标签', '未知主题'])[1],
            'theme_name': tags_info.get(tu[0], [None, None, '未知主题'])[2],
            'is_favorite': tu[1],
            'total_likes': tags_info.get(tu[0], [None, None, None, 0])[3],
            'click_count': tu[2]
        } for tu in tag_users]
        
        # 按主题分组
        grouped_result = {}
        for item in result:
            theme = item['theme_name'].lower()
            if theme not in grouped_result:
                grouped_result[theme] = []
            grouped_result[theme].append(item)
        
        # 构建详细偏好数据结构
        detailed_preferences = {}
        for theme, items in grouped_result.items():
            detailed_preferences[theme] = [
                {
                    'tag_id': item['tag_id'],
                    'score': item['click_count'] / 10 if item['click_count'] > 0 else 0.5  # 简单计算分数
                } for item in items
            ]
        
        # 构建最终响应
        response_data = {
            'detailed_preferences': detailed_preferences,
            'similar_users': [],  # 这里可以添加相似用户逻辑
            'raw_tags': result  # 保留原始数据
        }
        
        return JsonResponse({'code': 200, 'data': response_data})
    except Exception as e:
        print(f"获取用户标签状态出错: {str(e)}")
        return JsonResponse({'code': 500, 'message': str(e)})
    finally:
        cursor.close()
        conn.close()

@require_http_methods(["GET"])
def get_tag_by_theme_and_origin(request):
    """
    根据主题编号和原始ID获取标签ID
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        theme_name = request.GET.get('theme_name')
        origin_id = request.GET.get('origin_id')
        
        if not theme_name or not origin_id:
            return JsonResponse({
                'code': 400, 
                'message': '缺少必要参数：theme_name 或 origin_id'
            })
            
        print(f"查询主题 {theme_name} 下的原始ID {origin_id} 对应的标签")
        
        # 查询匹配的标签
        cursor.execute("""
            SELECT tag_id, tag_name, theme_name, total_clicks, total_likes
            FROM tag
            WHERE theme_name = %s AND origin_id = %s
        """, (theme_name, origin_id))
        
        tag = cursor.fetchone()
        
        if tag:
            result = {
                'id': tag[0],
                'tag_name': tag[1],
                'theme_name': tag[2],
                'total_clicks': tag[3],
                'total_likes': tag[4],
                'origin_id': origin_id
            }
            return JsonResponse({'code': 200, 'data': result})
        else:
            return JsonResponse({
                'code': 404, 
                'message': f'未找到主题 {theme_name} 下原始ID为 {origin_id} 的标签'
            })
            
    except Exception as e:
        print(f"查询标签出错: {str(e)}")
        return JsonResponse({'code': 500, 'message': str(e)})
    finally:
        cursor.close()
        conn.close()

@require_http_methods(["POST"])
def get_tags_by_theme_and_origins(request):
    """
    批量根据主题编号和原始ID列表获取标签ID
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        data = json.loads(request.body)
        theme_name = data.get('theme_name')
        origin_ids = data.get('origin_ids', [])
        
        if not theme_name or not origin_ids:
            return JsonResponse({
                'code': 400, 
                'message': '缺少必要参数：theme_name 或 origin_ids'
            })
            
        print(f"批量查询主题 {theme_name} 下的原始ID列表 {origin_ids} 对应的标签")
        
        # 构建 SQL IN 查询
        placeholders = ', '.join(['%s'] * len(origin_ids))
        query = f"""
            SELECT tag_id, tag_name, theme_name, total_clicks, total_likes, origin_id
            FROM tag
            WHERE theme_name = %s AND origin_id IN ({placeholders})
        """
        
        # 构建参数列表
        params = [theme_name] + origin_ids
        
        # 执行查询
        cursor.execute(query, params)
        tags = cursor.fetchall()
        
        if tags:
            results = [{
                'id': tag[0],
                'tag_name': tag[1],
                'theme_name': tag[2],
                'total_clicks': tag[3],
                'total_likes': tag[4],
                'origin_id': tag[5]
            } for tag in tags]
            
            # 创建一个映射，方便前端使用
            mapping = {str(tag['origin_id']): tag['id'] for tag in results}
            
            return JsonResponse({
                'code': 200, 
                'data': {
                    'tags': results,
                    'mapping': mapping  # origin_id 到 tag_id 的映射
                }
            })
        else:
            return JsonResponse({
                'code': 404, 
                'message': f'未找到主题 {theme_name} 下指定原始ID的标签'
            })
            
    except Exception as e:
        print(f"批量查询标签出错: {str(e)}")
        return JsonResponse({'code': 500, 'message': str(e)})
    finally:
        cursor.close()
        conn.close()
