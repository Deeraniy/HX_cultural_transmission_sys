from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
import pymysql
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64
import jieba
import jieba.posseg as pseg
import os
def get_cloud(request):
    # 从请求中获取spot_name
    spot_name = request.GET.get('name')

    # 创建连接
    conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                           db='hx_cultural_transmission_sys', charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # SQL查询，根据spot_name查找评论
    cursor.execute("SELECT spot_id FROM scenicspot WHERE spot_name=%s",(spot_name))
    spot_id=cursor.fetchone()['spot_id']
    cursor.execute("SELECT * FROM usercomment WHERE spot_id = %s", (spot_id))
    comments = cursor.fetchall()
        # 合并评论文本
    text = " ".join(comment['content'] for comment in comments)
    # print(text)
    words=pseg.cut(text)
    nouns = [word for word, flag in words if flag.startswith('n') and len(word) > 1]
    text = " ".join(nouns)
    # text = [word for word in jieba.cut(text) if len(word) > 1]
    # text = list(set(text))
    # text = " ".join(text)
    print(text)
    stopwords = ["这个","可以","一个","一下","一定","是不是","不是","什么","应该","我们","你们","他们","那个","怎么","然后","最后","因为","但是"]

        # 生成词云图
    
    wordcloud = WordCloud(collocations=False,width=800,height=800,font_path='C:\\Windows\\Fonts\\simhei.ttf', max_words=200, max_font_size=200, background_color=None, mode='RGBA',stopwords=stopwords).generate(text)
    image_path = os.path.join('static', 'wordclouds', f"{spot_name}_wordcloud.png")
    wordcloud.to_file(image_path)
    image_url = f"/static/wordclouds/{spot_name}_wordcloud.png"
    
    cursor.close()
    conn.close()
    return JsonResponse({'wordcloud_url': image_url})

def get_cloud_literature(request):
    # 从请求中获取liter_name
    liter_name = request.GET.get('name')

    # 创建连接
    conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                           db='hx_cultural_transmission_sys', charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # SQL查询，根据liter_name查找评论
    cursor.execute("SELECT liter_id FROM literature WHERE liter_name=%s", (liter_name,))
    liter_id = cursor.fetchone()['liter_id']
    cursor.execute("SELECT comment_text FROM user_comment_literature WHERE liter_id = %s", (liter_id,))
    comments = cursor.fetchall()

    # 合并评论文本
    text = " ".join(comment['comment_text'] for comment in comments)
    words = pseg.cut(text)
    nouns = [word for word, flag in words if flag.startswith('n') and len(word) > 1]
    text = " ".join(nouns)

    stopwords = ["这个", "可以", "一个", "一下", "一定", "是不是", "不是", "什么", "应该", "我们", "你们", "他们", "那个", "怎么", "然后", "最后", "因为", "但是"]

    # 生成词云图
    wordcloud = WordCloud(collocations=False, width=800, height=800, font_path='C:\\Windows\\Fonts\\simhei.ttf',
                          max_words=200, max_font_size=200, background_color=None, mode='RGBA', stopwords=stopwords).generate(text)
    image_path = os.path.join('static', 'wordclouds', f"{liter_name}_wordcloud.png")
    wordcloud.to_file(image_path)
    image_url = f"/static/wordclouds/{liter_name}_wordcloud.png"

    cursor.close()
    conn.close()
    return JsonResponse({'wordcloud_url': image_url})

def get_cloud_food(request):
    # 从请求中获取food_name
    food_name = request.GET.get('name')

    # 创建连接
    conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                           db='hx_cultural_transmission_sys', charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # SQL查询，根据food_name查找评论
    cursor.execute("SELECT food_id FROM food WHERE food_name=%s", (food_name,))
    food_id = cursor.fetchone()['food_id']
    cursor.execute("SELECT comment_text FROM user_comment_food WHERE food_id = %s", (food_id,))
    comments = cursor.fetchall()

    # 合并评论文本
    text = " ".join(comment['comment_text'] for comment in comments)
    words = pseg.cut(text)
    nouns = [word for word, flag in words if flag.startswith('n') and len(word) > 1]
    text = " ".join(nouns)

    stopwords = ["这个", "可以", "一个", "一下", "一定", "是不是", "不是", "什么", "应该", "我们", "你们", "他们", "那个", "怎么", "然后", "最后", "因为", "但是"]

    # 生成词云图
    wordcloud = WordCloud(collocations=False, width=800, height=800, font_path='C:\\Windows\\Fonts\\simhei.ttf',
                          max_words=200, max_font_size=200, background_color=None, mode='RGBA', stopwords=stopwords).generate(text)
    image_path = os.path.join('static', 'wordclouds', f"{food_name}_wordcloud.png")
    wordcloud.to_file(image_path)
    image_url = f"/static/wordclouds/{food_name}_wordcloud.png"

    cursor.close()
    conn.close()
    return JsonResponse({'wordcloud_url': image_url})

def get_cloud_folk(request):
    # 从请求中获取food_name
    folk_name = request.GET.get('name')

    # 创建连接
    conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                           db='hx_cultural_transmission_sys', charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # SQL查询，根据folk_name查找评论
    cursor.execute("SELECT folk_id FROM folk WHERE folk_name=%s", (folk_name,))
    folk_id = cursor.fetchone()['folk_id']
    cursor.execute("SELECT comment_text FROM user_comment_folk WHERE folk_id = %s", (folk_id,))
    comments = cursor.fetchall()

    # 合并评论文本
    text = " ".join(comment['comment_text'] for comment in comments)
    words = pseg.cut(text)
    nouns = [word for word, flag in words if flag.startswith('n') and len(word) > 1]
    text = " ".join(nouns)

    stopwords = ["这个", "可以", "一个", "一下", "一定", "是不是", "不是", "什么", "应该", "我们", "你们", "他们", "那个", "怎么", "然后", "最后", "因为", "但是"]

    # 生成词云图
    wordcloud = WordCloud(collocations=False, width=800, height=800, font_path='C:\\Windows\\Fonts\\simhei.ttf',
                          max_words=200, max_font_size=200, background_color=None, mode='RGBA', stopwords=stopwords).generate(text)
    image_path = os.path.join('static', 'wordclouds', f"{folk_name}_wordcloud.png")
    wordcloud.to_file(image_path)
    image_url = f"/static/wordclouds/{folk_name}_wordcloud.png"

    cursor.close()
    conn.close()
    return JsonResponse({'wordcloud_url': image_url})