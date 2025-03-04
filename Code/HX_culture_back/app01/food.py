from django.shortcuts import render, redirect,HttpResponse
import pymysql
import re
from django.http import JsonResponse
#修改
def get_food_list(request):
    # pass
    # 访问美食专区展示美食

    # 创建连接
    conn = pymysql.connect(host='60.215.128.117', port=15320, user='root', passwd='kissme77',
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
    conn = pymysql.connect(host='60.215.128.117', port=15320, user='root', passwd='kissme77',
                           db='hx_cultural_transmission_sys',charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)


    effect_row = cursor.execute("select * from food_influence left join food on food_influence.food_id=food.food_id")
    food_influence_list =cursor.fetchall()

    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return JsonResponse({"status": "ok", "data": food_influence_list})
    # 将查询得到的数据放在food_list列表中

def clearData():
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456',
                               db='hx_culture',charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 查询数据
    effect_row = cursor.execute("select * from folkcustom")

    # 获取所有记录
    records = cursor.fetchall()

    for record in records:
        # 去除 folk_name 中的【】内的内容
        folk_name = re.sub(r'【.*?】', '', record['folk_name'])

        # 提取 folk_img 中的图片地址
        folk_img = re.search(r'url\((.*?)\)', record['folk_img'])
        folk_img_url = folk_img.group(1) if folk_img else ''

        # 删除 folk_rank 中的前缀
        folk_rank = re.sub(r'级        别:', '', record['folk_rank'])

        # 删除 folk_type 中的前缀
        folk_type = re.sub(r'项目类别:', '', record['folk_type'])

        # 删除 batch 中的前缀
        batch = re.sub(r'批        次:', '', record['batch'])

        # 删除 text 的前缀
        text1 = re.sub(r'详情介绍', '', record['text'])
        text = re.sub(r' ', '', text1)




        # 更新记录
        update_query = """
        UPDATE folkcustom
        SET folk_name = %s, folk_rank = %s, folk_type = %s, batch = %s, text = %s
        WHERE id = %s
        """
        cursor.execute(update_query, (folk_name,  folk_rank, folk_type, batch, text, record['id']))
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    clearData()
