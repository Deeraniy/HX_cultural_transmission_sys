import numpy as np
import pandas as pd
import jieba
import re
import pymysql
import logging
from django.http import JsonResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# 配置日志
logger = logging.getLogger(__name__)

def get_topic_words(cursor, table_name, id_field, item_id):
    """从主题表中获取主题词"""
    cursor.execute(f"""
        SELECT topic_word, area, sentiment, frequency 
        FROM {table_name} 
        WHERE {id_field} = %s 
        ORDER BY topic_id
    """, [item_id])
    
    results = cursor.fetchall()
    if not results:
        return []
        
    # 将结果按每5个词组织成主题
    topics = []
    current_topic = []
    for word, area, sentiment, frequency in results:
        current_topic.append({
            'word': word,
            'sentiment': sentiment,
            'frequency': frequency
        })
        if len(current_topic) == 5:  # 每个主题5个词
            topics.append(current_topic)
            current_topic = []
            
    return topics

def process_topic_results(topics):
    """处理主题词并返回结果"""
    if not topics:
        return []
        
    result = []
    for topic_words in topics:
        # 直接使用数据库中存储的数据
        for word_info in topic_words:
            result.append({
                'topic': word_info['word'],
                'frequency': word_info['frequency'],
                'sentiment': word_info['sentiment']
            })
            
    return result

def lda_analyze(request):
    """处理景点的主题分析"""
    spot_name = request.GET.get('name')
    if not spot_name:
        return JsonResponse({'error': '景点名称不能为空'}, status=400)
        
    conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', 
                          passwd='song', db='hx_cultural_transmission_sys', 
                          charset='utf8')
    cursor = conn.cursor()
    
    try:
        # 获取景点ID
        cursor.execute("SELECT spot_id FROM spot WHERE spot_name = %s", [spot_name])
        result = cursor.fetchone()
        if not result:
            return JsonResponse({'error': f'未找到景点: {spot_name}'}, status=404)
            
        spot_id = result[0]
        
        # 获取主题词
        topics = get_topic_words(cursor, 'spot_topic', 'spot_id', spot_id)
        result = process_topic_results(topics)
        
        return JsonResponse(result, safe=False)
        
    except Exception as e:
        logger.error(f"处理景点 {spot_name} 的主题分析时出错: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        cursor.close()
        conn.close()

def lda_analyze_literature(request):
    """处理文学作品的主题分析"""
    liter_name = request.GET.get('name')
    if not liter_name:
        return JsonResponse({'error': '文学作品名称不能为空'}, status=400)
        
    conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', 
                          passwd='song', db='hx_cultural_transmission_sys', 
                          charset='utf8')
    cursor = conn.cursor()
    
    try:
        # 获取文学作品ID
        cursor.execute("SELECT liter_id FROM literature WHERE liter_name = %s", [liter_name])
        result = cursor.fetchone()
        if not result:
            return JsonResponse({'error': f'未找到文学作品: {liter_name}'}, status=404)
            
        liter_id = result[0]
        
        # 获取主题词
        topics = get_topic_words(cursor, 'liter_topic', 'liter_id', liter_id)
        result = process_topic_results(topics)
        
        return JsonResponse(result, safe=False)
        
    except Exception as e:
        logger.error(f"处理文学作品 {liter_name} 的主题分析时出错: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        cursor.close()
        conn.close()

def lda_analyze_food(request):
    """处理食品的主题分析"""
    food_name = request.GET.get('name')
    if not food_name:
        return JsonResponse({'error': '食品名称不能为空'}, status=400)
        
    conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', 
                          passwd='song', db='hx_cultural_transmission_sys', 
                          charset='utf8')
    cursor = conn.cursor()
    
    try:
        # 获取食品ID
        cursor.execute("SELECT food_id FROM food WHERE food_name = %s", [food_name])
        result = cursor.fetchone()
        if not result:
            return JsonResponse({'error': f'未找到食品: {food_name}'}, status=404)
            
        food_id = result[0]
        
        # 获取主题词
        topics = get_topic_words(cursor, 'food_topic', 'food_id', food_id)
        result = process_topic_results(topics)
        
        return JsonResponse(result, safe=False)
        
    except Exception as e:
        logger.error(f"处理食品 {food_name} 的主题分析时出错: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        cursor.close()
        conn.close()

def lda_analyze_folk(request):
    """处理民俗的主题分析"""
    folk_name = request.GET.get('name')
    if not folk_name:
        return JsonResponse({'error': '民俗名称不能为空'}, status=400)
        
    conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', 
                          passwd='song', db='hx_cultural_transmission_sys', 
                          charset='utf8')
    cursor = conn.cursor()
    
    try:
        # 获取民俗ID
        cursor.execute("SELECT folk_id FROM folk WHERE folk_name = %s", [folk_name])
        result = cursor.fetchone()
        if not result:
            return JsonResponse({'error': f'未找到民俗: {folk_name}'}, status=404)
            
        folk_id = result[0]
        
        # 获取主题词
        topics = get_topic_words(cursor, 'folk_topic', 'folk_id', folk_id)
        result = process_topic_results(topics)
        
        return JsonResponse(result, safe=False)
        
    except Exception as e:
        logger.error(f"处理民俗 {folk_name} 的主题分析时出错: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        cursor.close()
        conn.close()
