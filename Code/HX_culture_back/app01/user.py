from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
import pymysql
import json

# 实现注册
def register_user(request):
    if request.method == 'POST':
        try:
            # 从请求体获取 JSON 数据
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            age = data.get('age', 0)
            sex = data.get('sex', 'other')
            region = data.get('location', '')
            avatar = data.get('avatar', '')

            print(f"注册用户数据: {data}")  # 调试日志

            conn = pymysql.connect(host='60.215.128.117', port=15320, user='root', passwd='kissme77',
                                 db='hx_cultural_transmission_sys', charset='utf8')
            cursor = conn.cursor()
            
            try:
                # 检查用户名是否已存在
                check_sql = "SELECT user_id FROM user WHERE user_name = %s"
                cursor.execute(check_sql, (username,))
                if cursor.fetchone():
                    return JsonResponse({"status": "error", "msg": "用户名已存在"})

                # 执行插入
                sql = """
                INSERT INTO user 
                    (user_name, user_pwd, user_age, user_sex, user_region, user_avatar) 
                VALUES 
                    (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (username, password, age, sex, region, avatar))
                conn.commit()
                
                # 获取新插入用户的 ID
                new_user_id = cursor.lastrowid
                
                response_data = {
                    "status": "success",
                    "msg": "注册成功",
                    "user_id": new_user_id,
                    "username": username
                }
                print(f"注册成功: {response_data}")  # 调试日志
                return JsonResponse(response_data)

            except Exception as e:
                conn.rollback()
                print(f"注册错误: {str(e)}")  # 调试日志
                return JsonResponse({
                    "status": "error",
                    "msg": f"注册失败: {str(e)}"
                })
            finally:
                cursor.close()
                conn.close()
        except Exception as e:
            print(f"请求处理错误: {str(e)}")  # 调试日志
            return JsonResponse({
                "status": "error",
                "msg": f"请求处理失败: {str(e)}"
            })
    else:
        return JsonResponse({
            "status": "error",
            "msg": "请使用POST方法"
        })


def verify_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            print(f"尝试验证用户: {username}")

            conn = pymysql.connect(host='60.215.128.117', port=15320, user='root', passwd='kissme77',
                               db='hx_cultural_transmission_sys', charset='utf8')
            cursor = conn.cursor()
            try:
                sql = "SELECT user_id, user_name FROM user WHERE user_name = %s AND user_pwd = %s"
                cursor.execute(sql, (username, password))
                result = cursor.fetchone()
                
                print(f"查询结果: {result}")
                
                if result:
                    response_data = {
                        "status": "success",
                        "msg": "验证成功",
                        "user_id": result[0],
                        "username": result[1]
                    }
                    print(f"返回数据: {response_data}")  # 添加日志
                    return JsonResponse(response_data)
                else:
                    return JsonResponse({
                        "status": "error",
                        "msg": "验证失败：用户名或密码错误"
                    })
            except Exception as e:
                print(f"错误: {str(e)}")
                return JsonResponse({
                    "status": "error",
                    "msg": str(e)
                })
        except Exception as e:
            print(f"错误: {str(e)}")
            return JsonResponse({
                "status": "error",
                "msg": str(e)
            })
    else:
        return JsonResponse({
            "status": "error",
            "msg": "请使用POST方法"
        })


def get_user_activity(request):
    if request.method == 'GET':
        username = request.GET.get('username')

        if username:
            # 创建连接
            conn = pymysql.connect(host='60.215.128.117', port=15320, user='root', passwd='kissme77',
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
            conn = pymysql.connect(host='60.215.128.117', port=15320, user='root', passwd='kissme77',
                                   db='hx_cultural_transmission_sys', charset='utf8')
            cursor = conn.cursor()
            try:
                sql = """
                SELECT user_id, user_name, user_age, user_sex, user_region, user_avatar 
                FROM user 
                WHERE user_name = %s
                """
                cursor.execute(sql, (username,))
                result = cursor.fetchone()
                print("Query result:", result)
                
                if result:
                    user_info = {
                        'user_id': result[0],
                        'user_name': result[1],
                        'user_age': result[2],
                        'user_sex': result[3],  # 已经是字符串格式了
                        'user_region': result[4],
                        'user_avatar': result[5]
                    }
                    return JsonResponse(user_info)
                else:
                    return JsonResponse({"error": "用户不存在"})
            except Exception as e:
                conn.rollback()
                return JsonResponse({"error": f"获取用户信息失败: {e}"})
            finally:
                cursor.close()
                conn.close()
        else:
            return JsonResponse({"error": "未提供用户名"})
    else:
        return JsonResponse({"error": "不是GET请求!"})

def init_database():
    conn = pymysql.connect(
        host='60.215.128.117',
        port=15320,
        user='root',
        passwd='kissme77',
        db='hx_cultural_transmission_sys',
        charset='utf8'
    )
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            ALTER TABLE user MODIFY COLUMN user_id INT AUTO_INCREMENT PRIMARY KEY;
        """)
        conn.commit()
        print("数据库表结构更新成功")
    except Exception as e:
        conn.rollback()
        print(f"更新失败: {e}")
    finally:
        cursor.close()
        conn.close()

# 在文件末尾调用这个函数
if __name__ == "__main__":
    init_database()
