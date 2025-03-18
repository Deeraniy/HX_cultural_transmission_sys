from django.http import JsonResponse
from django.db import connection
from typing import List, Dict

def get_all_tags(request):
    """获取所有标签信息"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT tag_id, tag_name, theme_name, total_clicks, total_likes
            FROM tag
            ORDER BY theme_name, total_clicks DESC
        """)
        tags = cursor.fetchall()
        
        # 按主题分组整理数据
        theme_grouped_tags = {}
        for tag in tags:
            tag_id, tag_name, theme_name, total_clicks, total_likes = tag
            
            if theme_name not in theme_grouped_tags:
                theme_grouped_tags[theme_name] = []
                
            theme_grouped_tags[theme_name].append({
                'tag_id': tag_id,
                'tag_name': tag_name,
                'total_clicks': total_clicks,
                'total_likes': total_likes
            })
        
        return JsonResponse({
            'status': 'success',
            'data': theme_grouped_tags
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

def update_tag_interaction(request):
    """更新标签的点击或收藏状态"""
    try:
        data = request.POST
        user_id = data.get('user_id')
        tag_id = data.get('tag_id')
        action_type = data.get('action_type')  # 'click' or 'favorite'
        
        if not all([user_id, tag_id, action_type]):
            return JsonResponse({
                'status': 'error',
                'message': 'Missing required parameters'
            })
            
        cursor = connection.cursor()
        
        # 检查是否存在用户-标签关系
        cursor.execute("""
            SELECT click_count, is_favorite
            FROM tag_user
            WHERE user_id = %s AND tag_id = %s
        """, [user_id, tag_id])
        
        result = cursor.fetchone()
        
        if result:
            # 更新现有记录
            click_count, is_favorite = result
            if action_type == 'click':
                click_count += 1
                cursor.execute("""
                    UPDATE tag_user
                    SET click_count = %s
                    WHERE user_id = %s AND tag_id = %s
                """, [click_count, user_id, tag_id])
            elif action_type == 'favorite':
                new_favorite = not is_favorite
                cursor.execute("""
                    UPDATE tag_user
                    SET is_favorite = %s
                    WHERE user_id = %s AND tag_id = %s
                """, [new_favorite, user_id, tag_id])
        else:
            # 创建新记录
            cursor.execute("""
                INSERT INTO tag_user (user_id, tag_id, click_count, is_favorite)
                VALUES (%s, %s, %s, %s)
            """, [
                user_id,
                tag_id,
                1 if action_type == 'click' else 0,
                True if action_type == 'favorite' else False
            ])
        
        # 更新标签总统计
        if action_type == 'click':
            cursor.execute("""
                UPDATE tag
                SET total_clicks = total_clicks + 1
                WHERE tag_id = %s
            """, [tag_id])
        elif action_type == 'favorite':
            cursor.execute("""
                UPDATE tag
                SET total_likes = total_likes + 1
                WHERE tag_id = %s
            """, [tag_id])
        
        return JsonResponse({
            'status': 'success',
            'message': f'Successfully updated {action_type} for tag {tag_id}'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

def get_user_tag_status(request):
    """获取用户与标签的交互状态"""
    try:
        user_id = request.GET.get('user_id')
        
        if not user_id:
            return JsonResponse({
                'status': 'error',
                'message': 'Missing user_id parameter'
            })
            
        cursor = connection.cursor()
        cursor.execute("""
            SELECT tu.tag_id, t.tag_name, t.theme_name,
                   tu.click_count, tu.is_favorite
            FROM tag_user tu
            JOIN tag t ON tu.tag_id = t.tag_id
            WHERE tu.user_id = %s
        """, [user_id])
        
        user_tags = cursor.fetchall()
        
        # 整理数据
        tag_status = {}
        for tag in user_tags:
            tag_id, tag_name, theme_name, click_count, is_favorite = tag
            tag_status[tag_id] = {
                'tag_name': tag_name,
                'theme_name': theme_name,
                'click_count': click_count,
                'is_favorite': bool(is_favorite)
            }
            
        return JsonResponse({
            'status': 'success',
            'data': tag_status
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })
