from django.shortcuts import render, redirect,HttpResponse
import pymysql


def get_city_list(request):
    # pass
    # 访问classes的时候展示班级

    # 创建连接
    conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                           db='hx_cultural_transmission_sys',charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 执行SQL，并返回收影响行数
    effect_row = cursor.execute("select city_id,city_name from city")
    city_list =cursor.fetchall()
    print(city_list)

    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return HttpResponse(city_list)
    # 将查询得到的数据放在class_list列表中
    # return render(request,'classes.html',{'class_list':class_list})
