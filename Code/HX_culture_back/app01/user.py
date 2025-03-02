from django.shortcuts import render, redirect, HttpResponse, JsonResponse
import pymysql

# 实现注册
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 创建连接
        conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                               db='hx_cultural_transmission_sys', charset='utf8')
        # 创建游标
        cursor = conn.cursor()
        try:
            # 执行SQL插入语句
            sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(sql, (username, password))
            conn.commit()
            return HttpResponse("注册成功")
        except Exception as e:
            conn.rollback()
            return HttpResponse(f"注册失败: {e}")
        finally:
            # 关闭游标
            cursor.close()
            # 关闭连接
            conn.close()
    else:
        return HttpResponse("故障!")

# 获取用户浏览记录
def get_all_history(request):
    if request.method == 'GET':
        uid = request.GET.get('uid')
        if uid:
            # 创建连接
            conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                                   db='hx_cultural_transmission_sys', charset='utf8')
            # 创建游标
            cursor = conn.cursor()
            try:
                # 执行SQL查询语句
                sql = "SELECT * FROM browse_history WHERE uid = %s"
                cursor.execute(sql, (uid,))
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
        uid = request.POST.get('uid')
        item_id = request.POST.get('item_id')
        if uid and item_id:
            # 创建连接
            conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                                   db='hx_cultural_transmission_sys', charset='utf8')
            # 创建游标
            cursor = conn.cursor()
            try:
                # 执行SQL插入语句
                sql = "INSERT INTO browse_history (uid, item_id) VALUES (%s, %s)"
                cursor.execute(sql, (uid, item_id))
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
            return JsonResponse({"error": "未提供用户ID或项目ID"})
    else:
        return JsonResponse({"error": "不是POST请求!"})

# 删除浏览记录
def delete_history(request):
    if request.method == 'POST':
        history_id = request.POST.get('history_id')
        if history_id:
            # 创建连接
            conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                                   db='hx_cultural_transmission_sys', charset='utf8')
            # 创建游标
            cursor = conn.cursor()
            try:
                # 执行SQL删除语句
                sql = "DELETE FROM browse_history WHERE id = %s"
                cursor.execute(sql, (history_id,))
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
            return JsonResponse({"error": "未提供浏览记录ID"})
    else:
        return JsonResponse({"error": "不是POST请求!"})

# 更新浏览记录
def update_history(request):
    if request.method == 'POST':
        history_id = request.POST.get('history_id')
        uid = request.POST.get('uid')
        item_id = request.POST.get('item_id')
        if history_id and uid and item_id:
            # 创建连接
            conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                                   db='hx_cultural_transmission_sys', charset='utf8')
            # 创建游标
            cursor = conn.cursor()
            try:
                # 执行SQL更新语句
                sql = "UPDATE browse_history SET uid = %s, item_id = %s WHERE id = %s"
                cursor.execute(sql, (uid, item_id, history_id))
                conn.commit()
                return HttpResponse("更新成功")
            except Exception as e:
                conn.rollback()
                return HttpResponse(f"更新失败: {e}")
            finally:
                # 关闭游标
                cursor.close()
                # 关闭连接
                conn.close()
        else:
            return JsonResponse({"error": "未提供浏览记录ID、用户ID或项目ID"})
    else:
        return JsonResponse({"error": "不是POST请求!"})
