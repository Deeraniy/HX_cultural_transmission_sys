from django.shortcuts import render, redirect, HttpResponse
import pymysql
import json
from django.http import JsonResponse
from datetime import datetime
# 获取用户浏览记录
def get_all_history(request):
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
                    sql = "SELECT * FROM user_history WHERE uid = %s"
                    cursor.execute(sql, (uid,))
                elif username:
                    # 执行SQL查询语句根据username
                    sql = "SELECT * FROM user_history WHERE username = %s"
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
# 获取所有用户浏览记录
def get_history(request):
    if request.method == 'GET':
        uid = 'all'
        if uid:
            # 创建连接
            conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', passwd='song',
                                       db='hx_cultural_transmission_sys',charset='utf8')
            # 创建游标
            cursor = conn.cursor()
            try:
            # 执行SQL查询语句
                if uid:
                    sql = "SELECT * FROM user_history"
                    cursor.execute(sql)

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
# 添加浏览记录
def add_history(request):
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


def delete_history(request):
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


def delete_all_history(request):
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

def search_history(request):
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

