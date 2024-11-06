from transformers import pipeline
import pandas as pd
import logging
from django.shortcuts import render, redirect,HttpResponse
import pymysql
import json
from django.http import JsonResponse
# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 初始化情感分析模型
distilled_student_sentiment_classifier = pipeline(
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", 
    return_all_scores=True
)

def get_sentiment_label(text):
    """获取文本的情感标签和得分"""
    try:
        results = distilled_student_sentiment_classifier(text)[0]  # 获取分析结果
        # 找出得分最高的标签
        max_score_label = max(results, key=lambda x: x['score'])
        return max_score_label['label'], max_score_label['score']
    except Exception as e:
        logger.error(f"处理文本时出错: {text}. 错误信息: {str(e)}")
        return 'error', 0.0

def process_comments(comments_list):
    """处理评论列表并返回带标签的DataFrame"""
    results = []
    for comment in comments_list:
        label, score = get_sentiment_label(comment)
        results.append({
            'comment': comment,
            'sentiment': label,
            'confidence': score
        })
    return results

def sentiments_analyze(request):
    spot_name = request.GET.get('spot_name')
    conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                           db='hx_cultural_transmission_sys',charset='utf8')

    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    spot_id=cursor.execute("SELECT spot_id FROM scenicspot WHERE spot_name=%s",(spot_name))
    sql_query = "SELECT content FROM usercomment WHERE spot_id=%s"
    # 执行SQL，并返回收影响行数
    effect_row = cursor.execute(sql_query, (spot_id))
    comment_list =cursor.fetchall()
    print(comment_list)
    comment_list = [comment['content'] for comment in comment_list]
    results=process_comments(comment_list)
    cursor.close()
    conn.close()
    # 处理结果
    return JsonResponse(results, safe=False)

   

# 使用示例
if __name__ == "__main__":
    # 示例评论列表
    comments = [
        "今天真是个坏天气,才怪",
        "I love this movie and i would watch it again and again!",
        "这个产品质量太差了",
        "Service was just okay"
    ]
    
    # 处理评论
    results_df = process_comments(comments)
    logger.info(f"处理完成，结果如下：\n{results_df}")