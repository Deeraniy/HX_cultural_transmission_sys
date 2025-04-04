from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
import pymysql
import json
from django.db import connection
import os
from django.conf import settings
import base64
import time

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
            email = data.get('email', '')
            mobile = data.get('mobile', '')
            description = data.get('description', '')

            print(f"注册用户数据: {data}")  # 调试日志

            conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', passwd='song',
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
                    (user_name, user_pwd, user_age, user_sex, user_region,
                    user_avatar, email, mobile, description,
                    register_time, last_login_time)
                VALUES
                    (%s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    CURRENT_TIMESTAMP, NULL)
                """
                cursor.execute(sql, (
                    username, password, age, sex, region,
                    avatar, email, mobile, description
                ))
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

            conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', passwd='song',
                               db='hx_cultural_transmission_sys', charset='utf8')
            cursor = conn.cursor()
            try:
                sql = "SELECT user_id, user_name FROM user WHERE user_name = %s AND user_pwd = %s"
                cursor.execute(sql, (username, password))
                result = cursor.fetchone()

                print(f"查询结果: {result}")

                if result:
                    # 更新最后登录时间
                    update_sql = "UPDATE user SET last_login_time = CURRENT_TIMESTAMP WHERE user_id = %s"
                    cursor.execute(update_sql, (result[0],))

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
            conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', passwd='song',
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
    try:
        user_id = request.GET.get('userId')
        if not user_id:
            return JsonResponse({
                'status': 'error',
                'message': '未提供用户ID'
            })

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT user_id, user_name, user_sex, user_age, user_region,
                       user_avatar,description,email,mobile
                FROM user
                WHERE user_id = %s
            """, [user_id])

            user = cursor.fetchone()

            if user:
                return JsonResponse({
                    'status': 'success',
                    'data': {
                        'uid': user[0],
                        'account': user[0],
                        'nickname': user[1],
                        'gender': user[2] or '',
                        'age': user[3] or 0,
                        'location': user[4] or '',
                        'avatar': user[5] or '',
                        'description': user[6] or '',
                        'email': user[7] or '',
                        'mobile': user[8] or '',
                    }
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': '用户不存在'
                })

    except Exception as e:
        print('获取用户信息错误:', str(e))  # 添加错误日志
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

def init_database():
    conn = pymysql.connect(
        host='8.148.26.99',
        port=3306,
        user='root',
        passwd='song',
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

def update_user_info(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            uid = data.get('uid') or request.GET.get('userId')

            if not uid:
                return JsonResponse({
                    'status': 'error',
                    'message': '未提供用户ID'
                })

            # 获取要更新的字段
            nickname = data.get('nickname')
            gender = data.get('gender')
            # 转换性别值为数据库支持的格式
            if gender == '男':
                gender = 'male'
            elif gender == '女':
                gender = 'female'
            else:
                gender = 'other'

            age = data.get('age')
            description = data.get('description')
            location = data.get('location')
            description = data.get('description')
            email = data.get('email')
            mobile = data.get('mobile')
            with connection.cursor() as cursor:
                update_fields = []
                params = []

                if nickname is not None:
                    update_fields.append("user_name = %s")
                    params.append(nickname)
                if gender is not None:
                    update_fields.append("user_sex = %s")
                    params.append(gender)
                if age is not None:
                    update_fields.append("user_age = %s")
                    params.append(age)
                if description is not None:
                    update_fields.append("description = %s")
                    params.append(description)
                if location is not None:
                    update_fields.append("user_region = %s")
                    params.append(location)
                if description is not None:
                    update_fields.append("description = %s")
                    params.append(description)
                if email is not None:
                    update_fields.append("email = %s")
                    params.append(email)
                if mobile is not None:
                    update_fields.append("mobile = %s")
                    params.append(mobile)

                if update_fields:
                    params.append(uid)

                    sql = f"""
                        UPDATE user
                        SET {', '.join(update_fields)}
                        WHERE user_id = %s
                    """

                    try:
                        cursor.execute(sql, params)
                        if cursor.rowcount > 0:
                            return JsonResponse({
                                'status': 'success',
                                'message': '更新成功'
                            })
                        else:
                            return JsonResponse({
                                'status': 'error',
                                'message': '未找到要更新的用户'
                            })
                    except Exception as e:
                        print("SQL执行错误:", str(e))
                        return JsonResponse({
                            'status': 'error',
                            'message': f'数据库更新错误: {str(e)}'
                        })
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': '没有提供要更新的字段'
                    })
        else:
            return JsonResponse({
                'status': 'error',
                'message': '请使用POST方法'
            })
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': '无效的JSON数据'
        })
    except Exception as e:
        print("更新用户信息错误:", str(e))
        return JsonResponse({
            'status': 'error',
            'message': f'服务器错误: {str(e)}'
        })

def upload_avatar(request):
    if request.method == 'POST':
        try:
            file = request.FILES.get('file')
            user_id = request.POST.get('userId')

            if not file or not user_id:
                return JsonResponse({
                    'status': 'error',
                    'message': '没有收到文件或用户ID'
                })

            # 读取文件内容并转换为base64
            file_content = base64.b64encode(file.read()).decode('utf-8')

            # 获取文件类型
            file_type = file.content_type

            # 生成完整的base64图片字符串
            avatar_data = f"data:{file_type};base64,{file_content}"

            # 更新数据库中的头像
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE user
                    SET user_avatar = %s
                    WHERE user_id = %s
                """, [avatar_data, user_id])

            return JsonResponse({
                'status': 'success',
                'data': {
                    'url': avatar_data
                }
            })

        except Exception as e:
            print(f"上传错误: {str(e)}")  # 添加错误日志
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })

    return JsonResponse({
        'status': 'error',
        'message': '不支持的请求方法'
    })

# 在文件末尾调用这个函数
if __name__ == "__main__":
    init_database()
