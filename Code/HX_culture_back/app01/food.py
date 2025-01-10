from django.shortcuts import render, redirect,HttpResponse
import pymysql
from django.http import JsonResponse
def get_food_list(request):
    # pass
    # 访问美食专区展示美食

    # 创建连接
    conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                           db='hx_cultural_transmission_sys',charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 执行SQL，并返回收影响行数
    effect_row = cursor.execute("select food_id,food_name,description,image_url from food")
    food_list =cursor.fetchall()
    print(food_list)

    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return JsonResponse({"status": "ok", "data": food_list})
    # 将查询得到的数据放在food_list列表中

def get_food_influence(request):
    # pass
    # 访问美食专区展示美食

    # 创建连接
    conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                           db='hx_cultural_transmission_sys',charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)


    effect_row = cursor.execute("select * from food_influence")
    food_list =cursor.fetchall()
    print(food_list)

    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return HttpResponse(food_list)
    # 将查询得到的数据放在food_list列表中
