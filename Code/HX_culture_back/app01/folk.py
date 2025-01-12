from django.shortcuts import render, redirect,HttpResponse
import pymysql
from django.http import JsonResponse

def get_folkcustom_list(request):
    # pass
    # 访问非遗文化专区展示非遗民俗
    # 创建连接
    conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                           db='hx_cultural_transmission_sys',charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 执行SQL，并返回收影响行数
    effect_row = cursor.execute("select folk_name,image_url,folk_type,folk_rank,description from folk")
    #folk和folkcustom表内容一样
    folkcustom_list =cursor.fetchall()
    print(folkcustom_list)

    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return JsonResponse({"status": "ok", "data": folkcustom_list})
    # 将查询得到的数据放在food_list列表中

def get_folk_influence(request):
    # pass
    # 访问非遗文化专区展示非遗传播效果

    # 创建连接
    conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                           db='hx_cultural_transmission_sys',charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)


    effect_row = cursor.execute("select * from folk_influence")
    folk_influence_list =cursor.fetchall()

    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return JsonResponse({"status": "ok", "data": folk_influence_list})
    # 将查询得到的数据放在food_list列表中
