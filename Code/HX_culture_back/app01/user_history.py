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

# 删除指定的用户历史记录
def delete_user_history(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            uid = data.get('uid')
            history_ids = data.get('history_ids')
            
            if not uid or not history_ids or not isinstance(history_ids, list):
                return JsonResponse({"error": "请提供有效的用户ID和历史记录ID列表"}, status=400)
            
            # 确保uid和history_ids都是整数类型
            try:
                uid = int(uid)
                history_ids = [int(hid) for hid in history_ids]
            except (ValueError, TypeError):
                return JsonResponse({"error": "用户ID和历史记录ID必须是数字"}, status=400)
            
            # 创建连接
            conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', passwd='song',
                                db='hx_cultural_transmission_sys', charset='utf8')
            cursor = conn.cursor()
            
            try:
                if len(history_ids) == 1:
                    # 单条删除
                    sql = "DELETE FROM user_history WHERE uid = %s AND id = %s"
                    cursor.execute(sql, (uid, history_ids[0]))
                else:
                    # 批量删除 - 使用更安全的参数传递方式
                    placeholders = ', '.join(['%s'] * len(history_ids))
                    sql = f"DELETE FROM user_history WHERE uid = %s AND id IN ({placeholders})"
                    params = [uid] + history_ids
                    cursor.execute(sql, params)
                
                conn.commit()
                return JsonResponse({"status": "success", "message": "删除成功", "deleted_count": cursor.rowcount})
            except Exception as e:
                conn.rollback()
                # 打印详细错误信息以便调试
                import traceback
                error_msg = traceback.format_exc()
                print(f"删除历史记录错误: {error_msg}")
                return JsonResponse({"error": f"删除失败: {str(e)}"}, status=500)
            finally:
                cursor.close()
                conn.close()
        except json.JSONDecodeError as e:
            return JsonResponse({"error": f"无效的JSON数据: {str(e)}"}, status=400)
        except Exception as e:
            # 捕获所有其他异常
            import traceback
            error_msg = traceback.format_exc()
            print(f"其他错误: {error_msg}")
            return JsonResponse({"error": f"处理请求时出错: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "不是POST请求!"}, status=405)

# 清空用户所有历史记录
def clear_user_history(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            uid = data.get('uid')
            
            if not uid:
                return JsonResponse({"error": "请提供有效的用户ID"}, status=400)
            
            # 确保uid是整数类型
            try:
                uid = int(uid)
            except (ValueError, TypeError):
                return JsonResponse({"error": "用户ID必须是数字"}, status=400)
            
            # 创建连接
            conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', passwd='song',
                                db='hx_cultural_transmission_sys', charset='utf8')
            cursor = conn.cursor()
            
            try:
                # 执行SQL删除语句
                sql = "DELETE FROM user_history WHERE uid = %s"
                cursor.execute(sql, (uid,))
                conn.commit()
                
                return JsonResponse({
                    "status": "success", 
                    "message": "已清空所有历史记录", 
                    "deleted_count": cursor.rowcount
                })
            except Exception as e:
                conn.rollback()
                # 打印详细错误信息以便调试
                import traceback
                error_msg = traceback.format_exc()
                print(f"清空历史记录错误: {error_msg}")
                return JsonResponse({"error": f"清空历史记录失败: {str(e)}"}, status=500)
            finally:
                cursor.close()
                conn.close()
        except json.JSONDecodeError as e:
            return JsonResponse({"error": f"无效的JSON数据: {str(e)}"}, status=400)
        except Exception as e:
            # 捕获所有其他异常
            import traceback
            error_msg = traceback.format_exc()
            print(f"其他错误: {error_msg}")
            return JsonResponse({"error": f"处理请求时出错: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "不是POST请求!"}, status=405)

def delete_all_history(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        if username:
            # 创建连接
            conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', passwd='song',
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
            conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', passwd='song',
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

