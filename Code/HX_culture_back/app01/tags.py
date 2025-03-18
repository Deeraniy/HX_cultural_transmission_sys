from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import pymysql
import json

def get_db_connection():
    return pymysql.connect(
        host='60.215.128.117',
        port=15320,
        user='root',
        passwd='kissme77',
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
        
        conn.commit()
        return JsonResponse({'code': 200, 'message': '浏览记录已更新'})
    except Exception as e:
        conn.rollback()
        return JsonResponse({'code': 500, 'message': str(e)})
    finally:
        cursor.close()
        conn.close()

@require_http_methods(["POST"])
def toggle_like(request):
    """
    切换标签点赞状态（增加或减少点赞数）
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        tag_id = data.get('tag_id')
        
        print(f"接收到点赞请求，user_id: {user_id}, tag_id: {tag_id}")
        
        # 先检查tag是否存在
        cursor.execute("SELECT tag_id, total_likes FROM tag WHERE tag_id = %s", (tag_id,))
        tag_info = cursor.fetchone()
        
        if not tag_info:
            print(f"错误: 找不到tag_id为{tag_id}的标签")
            return JsonResponse({'code': 404, 'message': f'找不到ID为{tag_id}的标签'})
        
        # 检查用户是否已经点赞过这个标签
        cursor.execute("""
            SELECT is_liked FROM tag_user 
            WHERE user_id = %s AND tag_id = %s
        """, (user_id, tag_id))
        user_tag = cursor.fetchone()
        
        # 默认为未点赞状态
        is_liked = False
        
        if user_tag is not None:
            # 用户记录存在，切换点赞状态
            is_liked = bool(user_tag[0])
            new_is_liked = not is_liked
            
            # 更新用户点赞状态
            cursor.execute("""
                UPDATE tag_user 
                SET is_liked = %s 
                WHERE user_id = %s AND tag_id = %s
            """, (new_is_liked, user_id, tag_id))
            
            # 更新标签总点赞数
            like_change = 1 if new_is_liked else -1
            cursor.execute("""
                UPDATE tag 
                SET total_likes = total_likes + %s 
                WHERE tag_id = %s
            """, (like_change, tag_id))
        else:
            # 用户记录不存在，创建新记录并设为已点赞
            cursor.execute("""
                INSERT INTO tag_user (user_id, tag_id, click_count, is_favorite, is_liked) 
                VALUES (%s, %s, 0, 0, 1)
            """, (user_id, tag_id))
            
            # 增加标签总点赞数
            cursor.execute("""
                UPDATE tag 
                SET total_likes = total_likes + 1 
                WHERE tag_id = %s
            """, (tag_id,))
            new_is_liked = True
        
        # 获取更新后的总点赞数
        cursor.execute("""
            SELECT COALESCE(total_likes, 0) as total_likes 
            FROM tag 
            WHERE tag_id = %s
        """, (tag_id,))
        total_likes = cursor.fetchone()[0]
        print(f"更新后的点赞数: {total_likes}, 点赞状态: {new_is_liked}")
        
        conn.commit()
        return JsonResponse({
            'code': 200,
            'message': '操作成功',
            'data': {
                'total_likes': total_likes,
                'is_liked': new_is_liked
            }
        })
    except Exception as e:
        print(f"Error in toggle_like: {str(e)}")
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
    获取标签的状态（点赞数、是否收藏）
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        user_id = request.GET.get('user_id')
        tag_id = request.GET.get('tag_id')
        
        # 获取标签总点赞数
        cursor.execute("""
            SELECT COALESCE(total_likes, 0) as total_likes 
            FROM tag 
            WHERE tag_id = %s
        """, (tag_id,))
        tag_result = cursor.fetchone()
        
        # 获取用户-标签关系 (包含is_liked)
        cursor.execute("""
            SELECT 
                COALESCE(is_favorite, 0) as is_favorite,
                COALESCE(click_count, 0) as click_count,
                COALESCE(is_liked, 0) as is_liked
            FROM tag_user 
            WHERE user_id = %s AND tag_id = %s
        """, (user_id, tag_id))
        user_tag = cursor.fetchone()
        
        return JsonResponse({
            'code': 200,
            'data': {
                'total_likes': tag_result[0] if tag_result else 0,
                'is_liked': bool(user_tag[2]) if user_tag else False,  # 正确返回用户点赞状态
                'is_favorite': bool(user_tag[0]) if user_tag else False,
                'click_count': user_tag[1] if user_tag else 0
            }
        })
    except Exception as e:
        print(f"Error in get_tag_status: {str(e)}")
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
