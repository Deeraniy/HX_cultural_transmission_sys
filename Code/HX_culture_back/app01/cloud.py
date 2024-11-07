from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
import pymysql
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64
import jieba
import os
def get_cloud(request):
    # 从请求中获取spot_name
    spot_name = request.GET.get('spot_name')

    # 创建连接
    conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                           db='hx_cultural_transmission_sys', charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # SQL查询，根据spot_name查找评论
    spot_id=cursor.execute("SELECT spot_id FROM scenicspot WHERE spot_name=%s",(spot_name))
    cursor.execute("SELECT * FROM usercomment WHERE spot_id = %s", (spot_id))
    comments = cursor.fetchall()
    print(comments)
        # 合并评论文本
    text = " ".join(comment['content'] for comment in comments)
    text = [word for word in jieba.cut(text) if len(word) > 1]
    text = list(set(text))
    text = " ".join(text)
    print(text)

        # 生成词云图
    
    wordcloud = WordCloud(width=800,height=800,font_path='C:\\Windows\\Fonts\\simhei.ttf', max_words=200, max_font_size=100, background_color=None).generate(text)
    image_path = os.path.join('static', 'wordclouds', f"{spot_name}_wordcloud.png")
    wordcloud.to_file(image_path)
    image_url = f"/static/wordclouds/{spot_name}_wordcloud.png"
    
        
    cursor.close()
    conn.close()
    return JsonResponse({'wordcloud_url': image_url})
