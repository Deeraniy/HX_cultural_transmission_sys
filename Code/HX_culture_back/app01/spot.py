from django.shortcuts import render, redirect,HttpResponse
import pymysql


def get_spot_list(request):
    # pass
    # 访问classes的时候展示班级

    # 创建连接
    conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', passwd='song',
                           db='hx_cultural_transmission_sys',charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 执行SQL，并返回收影响行数
    effect_row = cursor.execute("select * from spot")
    spot_list =cursor.fetchall()
    print(spot_list)

    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return HttpResponse(spot_list)
    # 将查询得到的数据放在class_list列表中
    # return render(request,'classes.html',{'class_list':class_list})

def get_spot_by_name(request):
    spot_name=request.GET.get('spot_name')
    conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', passwd='song',
                           db='hx_cultural_transmission_sys',charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql_query = "select * from spot where spot_name like %s"
    effect_row=cursor.execute(sql_query,('%'+spot_name+'%'))
    spot_list=cursor.fetchall()
    cursor.close()
    conn.close()
    return HttpResponse(spot_list)