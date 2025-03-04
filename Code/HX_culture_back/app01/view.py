from django.shortcuts import render, redirect,HttpResponse
import pymysql


def classes(request):
    # pass
    # 访问classes的时候展示班级

    # 创建连接
    conn = pymysql.connect(host='60.215.128.117', port=15320, user='root', passwd='kissme77',
                           db='studentmanagement',charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 执行SQL，并返回收影响行数
    effect_row = cursor.execute("select id,title from class")
    class_list =cursor.fetchall()
    print(class_list)

    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    # 将查询得到的数据放在class_list列表中
    return render(request,'classes.html',{'class_list':class_list})
