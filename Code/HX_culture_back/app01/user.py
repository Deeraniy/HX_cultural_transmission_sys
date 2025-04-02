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
            # 处理地区数据
            location = data.get('location', '')
            # 如果是中国地区，保持原有的区域代码格式
            if isinstance(location, list) and len(location) > 0:
                region = location[-1]  # 使用最后一级区域代码
            else:
                region = location  # 国际地区直接使用国家名称
            avatar = data.get('avatar', '')
            email = data.get('email', '')
            mobile = data.get('mobile', '')
            description = data.get('description', '')

            print(f"注册用户数据: {data}")  # 调试日志
            print(f"处理后的地区: {region}")  # 调试日志

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
                       user_avatar
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
                        'description': '这个人很懒，什么都没写~',
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

def get_user_distribution(request):
    if request.method == 'GET':
        try:
            conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', passwd='song',
                               db='hx_cultural_transmission_sys', charset='utf8')
            cursor = conn.cursor()

            # 主题名称映射
            theme_name_map = {
                'spot': '名胜古迹',
                'food': '美食文化',
                'literature': '影视文学',
                'folk': '非遗民俗'
            }

            # 修改SQL查询，获取每个用户点击最多的主题
            sql = """
            SELECT 
                u.user_id,
                u.user_region,
                t.theme_name,
                tu.click_count
            FROM user u
            LEFT JOIN tag_user tu ON u.user_id = tu.user_id
            LEFT JOIN tag t ON tu.tag_id = t.tag_id
            WHERE u.user_region IS NOT NULL 
            AND u.user_region != ''
            AND tu.click_count = (
                SELECT MAX(tu2.click_count)
                FROM tag_user tu2
                WHERE tu2.user_id = u.user_id
            )
            """

            cursor.execute(sql)
            results = cursor.fetchall()

            # 格式化数据
            distribution_data = {}
            for row in results:
                user_id, region, theme, clicks = row  # 现在正好是 4 个值
                
                if not region:
                    continue

                # 处理地区信息
                if region.isdigit():
                    normalized_region = "China"
                elif region == 'hunan':
                    normalized_region = "China"
                elif region == 'heilongjiang':
                    normalized_region = "China"
                else:
                    normalized_region = region

                # 初始化地区数据
                if normalized_region not in distribution_data:
                    distribution_data[normalized_region] = {
                        'total': 0,
                        'themes': {
                            '名胜古迹': set(),
                            '美食文化': set(),
                            '影视文学': set(),
                            '非遗民俗': set()
                        },
                        'users': set()
                    }

                distribution_data[normalized_region]['users'].add(user_id)

                # 只添加用户最常浏览的主题
                if theme:
                    print(f"主题: {theme}")
                    chinese_theme = theme_name_map.get(theme)
                    if chinese_theme:
                        print(f"添加用户 {user_id} 到地区 {normalized_region} 的主题 {chinese_theme} (点击次数: {clicks})")
                        distribution_data[normalized_region]['themes'][chinese_theme].add(user_id)

            # 处理最终数据
            for region in distribution_data:
                # 计算总用户数
                distribution_data[region]['total'] = len(distribution_data[region]['users'])
                # 转换主题的用户集合为用户数量
                for theme in distribution_data[region]['themes']:
                    distribution_data[region]['themes'][theme] = len(distribution_data[region]['themes'][theme])
                # 删除用户集合
                del distribution_data[region]['users']

            return JsonResponse({
                'status': 'success',
                'data': distribution_data
            })

        except Exception as e:
            print(f"\n获取用户分布数据错误:\n错误类型: {type(e)}\n错误信息: {str(e)}\n")
            import traceback
            print("详细错误信息:")
            print(traceback.format_exc())
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
        finally:
            cursor.close()
            conn.close()
            print("数据库连接已关闭")
    else:
        print(f"收到非GET请求: {request.method}")
        return JsonResponse({
            'status': 'error',
            'message': '请使用GET方法'
        })

# 在文件末尾调用这个函数
if __name__ == "__main__":
    init_database()
