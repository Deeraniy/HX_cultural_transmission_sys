from django.shortcuts import render, redirect,HttpResponse
from django.http import JsonResponse
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


def verify_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 创建连接
        conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                               db='hx_cultural_transmission_sys', charset='utf8')
        # 创建游标
        cursor = conn.cursor()
        try:
            # 执行SQL查询语句
            sql = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(sql, (username, password))
            result = cursor.fetchone()
            if result:
                return HttpResponse("验证成功")
            else:
                return HttpResponse("验证失败: 用户名或密码错误")
        except Exception as e:
            conn.rollback()
            return HttpResponse(f"验证失败: {e}")
        finally:
            # 关闭游标
            cursor.close()
            # 关闭连接
            conn.close()
    else:
        return HttpResponse("故障!")


def get_user_activity(request):
    if request.method == 'GET':
        username = request.GET.get('username')

        if username:
            # 创建连接
            conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                                   db='hx_cultural_transmission_sys', charset='utf8')
            # 创建游标
            cursor = conn.cursor()
            try:
                # 获取浏览记录
                sql_history = """
                SELECT * FROM user_history WHERE username = %s
                """
                cursor.execute(sql_history, (username,))
                history_results = cursor.fetchall()
                history_columns = [desc[0] for desc in cursor.description]
                history_data = [dict(zip(history_columns, row)) for row in history_results]

                # 获取收藏记录
                sql_star = """
                SELECT * FROM user_star WHERE username = %s
                """
                cursor.execute(sql_star, (username,))
                star_results = cursor.fetchall()
                star_columns = [desc[0] for desc in cursor.description]
                star_data = [dict(zip(star_columns, row)) for row in star_results]

                # 统计每个分类type的数量
                sql_type_count = """
                SELECT type, COUNT(*) as count FROM (
                    SELECT type FROM user_history WHERE username = %s
                    UNION ALL
                    SELECT type FROM user_star WHERE username = %s
                ) AS combined
                GROUP BY type
                """
                cursor.execute(sql_type_count, (username, username))
                type_count_results = cursor.fetchall()
                type_count_data = {row[0]: row[1] for row in type_count_results}

                # 返回结果
                return JsonResponse({
                    "history": history_data,
                    "star": star_data,
                    "type_count": type_count_data
                }, safe=False)
            except Exception as e:
                conn.rollback()
                return JsonResponse({"error": f"获取用户活动数据失败: {e}"})
            finally:
                # 关闭游标
                cursor.close()
                # 关闭连接
                conn.close()
        else:
            return JsonResponse({"error": "未提供用户名"})
    else:
        return JsonResponse({"error": "不是GET请求!"})

def get_user_info(request):
    if request.method == 'GET':
        username = request.GET.get('username')

        if username:
            # 创建连接
            conn = pymysql.connect(host='60.215.128.117', port=15320, user='root', passwd='kissme77',
                                   db='hx_cultural_transmission_sys', charset='utf8')
            # 创建游标
            cursor = conn.cursor()
            try:
                # 执行SQL查询语句
                sql = "SELECT * FROM users WHERE username = %s"
                cursor.execute(sql, (username,))
                result = cursor.fetchone()
                if result:
                    columns = [desc[0] for desc in cursor.description]
                    user_info = dict(zip(columns, result))
                    return JsonResponse(user_info)
                else:
                    return JsonResponse({"error": "用户不存在"})
            except Exception as e:
                conn.rollback()
                return JsonResponse({"error": f"获取用户信息失败: {e}"})
            finally:
                # 关闭游标
                cursor.close()
                # 关闭连接
                conn.close()
        else:
            return JsonResponse({"error": "未提供用户名"})
    else:
        return JsonResponse({"error": "不是GET请求!"})
