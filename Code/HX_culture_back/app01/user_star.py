from django.shortcuts import render, redirect, HttpResponse
import pymysql
import json
from django.http import JsonResponse
from datetime import datetime
# 获取用户浏览记录
def get_all_star(request):
    if request.method == 'GET':
        uid = request.GET.get('uid')
        username = request.GET.get('username')
        if uid or username:
            # 创建连接
            conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', passwd='song',
                                       db='hx_cultural_transmission_sys',charset='utf8')
            # 创建游标
            cursor = conn.cursor()
            try:
            # 执行SQL查询语句
                if uid:
                    sql = """
                    SELECT DISTINCT tu.user_id, tu.tag_id, tu.is_favorite, tu.click_count, t.*, uh.img_url 
                    FROM tag_user tu 
                    LEFT JOIN tag t ON tu.tag_id = t.tag_id 
                    LEFT JOIN user_history uh ON t.tag_name = uh.name
                    WHERE tu.user_id = %s AND tu.is_favorite = 1
                    GROUP BY tu.tag_id
                    """
                    cursor.execute(sql, (uid,))
                elif username:
                    # 执行SQL查询语句根据username，增加关联查询user_history获取img_url
                    sql = """
                    SELECT DISTINCT us.*, uh.img_url 
                    FROM user_star us
                    LEFT JOIN user_history uh ON us.name = uh.name AND us.type = uh.type
                    WHERE us.username = %s
                    GROUP BY us.id
                    """
                    cursor.execute(sql, (username,))

                results = cursor.fetchall()
                # 将查询结果转换为字典列表
                columns = [desc[0] for desc in cursor.description]
                data = [dict(zip(columns, row)) for row in results]
                return JsonResponse(data, safe=False)
            except Exception as e:
                conn.rollback()
                return JsonResponse({"error": f"获取用户数据失败: {e}"})
            finally:
                # 关闭游标
                cursor.close()
                # 关闭连接
                conn.close()
        else:
            return JsonResponse({"error": "未提供用户ID"})
    else:
        return JsonResponse({"error": "不是GET请求!"})

# 添加新函数：更新收藏状态
def update_favorite(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            tag_id = data.get('tag_id')
            is_favorite = data.get('is_favorite', 0)
            
            if not user_id or not tag_id:
                return JsonResponse({"error": "缺少必要参数：user_id或tag_id"})
                
            # 创建连接
            conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', passwd='song',
                                  db='hx_cultural_transmission_sys', charset='utf8')
            # 创建游标
            cursor = conn.cursor()
            try:
                # 更新收藏状态
                sql = "UPDATE tag_user SET is_favorite = %s WHERE user_id = %s AND tag_id = %s"
                cursor.execute(sql, (is_favorite, user_id, tag_id))
                conn.commit()
                
                return JsonResponse({"success": True, "message": "收藏状态更新成功"})
            except Exception as e:
                conn.rollback()
                return JsonResponse({"error": f"更新收藏状态失败: {e}"})
            finally:
                cursor.close()
                conn.close()
        except Exception as e:
            return JsonResponse({"error": f"请求处理失败: {e}"})
    else:
        return JsonResponse({"error": "仅支持POST请求"})

# 添加浏览记录
def add_star(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        uid = data.get('uid')
        type = data.get('type')
        name = data.get('name')
        img_url = data.get('img_url')
        describe = data.get('describe')

        if uid:
            # 创建连接
            conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', passwd='song',
                                   db='hx_cultural_transmission_sys',charset='utf8')
            # 创建游标
            cursor = conn.cursor()
            try:
                # 执行SQL插入语句
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                sql = "INSERT INTO user_history (uid, type, name, img_url, history_describe,history_time) VALUES (%s, %s, %s, %s, %s,%s)"
                cursor.execute(sql, (uid, type, name, img_url, describe, time))
                conn.commit()
                return HttpResponse("添加成功")
            except Exception as e:
                conn.rollback()
                return HttpResponse(f"添加失败: {e}")
            finally:
                # 关闭游标
                cursor.close()
                # 关闭连接
                conn.close()
        else:
            return JsonResponse({"error": "未提供用户ID、类型、名称、图片URL或描述"})
    else:
        return JsonResponse({"error": "不是POST请求!"})


def delete_star(request):
     if request.method == 'POST':
         username = request.POST.get('username')
         type_ = request.POST.get('type')
         name = request.POST.get('name')

         if username and type_ and name:
             # 创建连接
             conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', passwd='song',
                                        db='hx_cultural_transmission_sys',charset='utf8')
             # 创建游标
             cursor = conn.cursor()
             try:
                 # 执行SQL删除语句
                 sql = "DELETE FROM browse_history WHERE username = %s AND type = %s AND name = %s"
                 cursor.execute(sql, (username, type_, name))
                 conn.commit()
                 return HttpResponse("删除成功")
             except Exception as e:
                 conn.rollback()
                 return HttpResponse(f"删除失败: {e}")
             finally:
                 # 关闭游标
                 cursor.close()
                 # 关闭连接
                 conn.close()
         else:
             return JsonResponse({"error": "未提供用户名、类型或名称"})
     else:
         return JsonResponse({"error": "不是POST请求!"})


def delete_all_star(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        if username:
            # 创建连接
            conn = pymysql.connect(host='120.233.26.237', port=3306, user='root', passwd='song',
                                   db='hx_cultural_transmission_sys', charset='utf8')
            # 创建游标
            cursor = conn.cursor()
            try:
                # 执行SQL删除语句
                sql = "DELETE FROM username_history WHERE username = %s"
                cursor.execute(sql, (username,))
                conn.commit()
                return HttpResponse("全部删除成功")
            except Exception as e:
                conn.rollback()
                return HttpResponse(f"删除失败: {e}")
            finally:
                # 关闭游标
                cursor.close()
                # 关闭连接
                conn.close()
        else:
            return JsonResponse({"error": "未提供用户名"})
    else:
        return JsonResponse({"error": "不是POST请求!"})

def search_star(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        keyword = request.GET.get('keyword')

        if username and keyword:
            # 创建连接
            conn = pymysql.connect(host='120.233.26.237', port=3306, user='root', passwd='song',
                                   db='hx_cultural_transmission_sys', charset='utf8')
            # 创建游标
            cursor = conn.cursor()
            try:
                # 执行SQL查询语句
                sql = """
                SELECT * FROM user_history
                WHERE username = %s
                AND (name LIKE %s OR describe LIKE %s)
                """
                cursor.execute(sql, (username, f'%{keyword}%', f'%{keyword}%'))
                results = cursor.fetchall()
                # 将查询结果转换为字典列表
                columns = [desc[0] for desc in cursor.description]
                data = [dict(zip(columns, row)) for row in results]
                return JsonResponse(data, safe=False)
            except Exception as e:
                conn.rollback()
                return JsonResponse({"error": f"搜索用户数据失败: {e}"})
            finally:
                # 关闭游标
                cursor.close()
                # 关闭连接
                conn.close()
        else:
            return JsonResponse({"error": "未提供用户名或提示词"})
    else:
        return JsonResponse({"error": "不是GET请求!"})

