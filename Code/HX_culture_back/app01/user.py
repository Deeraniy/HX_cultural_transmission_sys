from django.shortcuts import render, redirect,HttpResponse
import pymysql

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
