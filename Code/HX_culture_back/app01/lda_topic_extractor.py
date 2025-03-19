import numpy as np
import pandas as pd
import jieba
import re
import pymysql
import logging
from django.http import JsonResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from .spot_sentiments_analyze import process_comments

# 配置日志
logger = logging.getLogger(__name__)

def top_words_data_frame(model: LatentDirichletAllocation, 
                        tf_idf_vectorizer: TfidfVectorizer, 
                        n_top_words: int) -> pd.DataFrame:
    """获取每个主题的前N个主题词"""
    rows = []
    feature_names = tf_idf_vectorizer.get_feature_names_out()
    for topic in model.components_:
        top_words = [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
        rows.append(top_words)
    columns = [f'topic word {i+1}' for i in range(n_top_words)]
    df = pd.DataFrame(rows, columns=columns)
    return df

def calculate_word_frequency(comments, topic_words):
    """计算主题词在评论中的出现频率"""
    word_freq = {}
    for word in topic_words:
        word_freq[word] = sum(comment.count(word) for comment in comments)
    return word_freq

# 其他配置参数
n_topics = 5  # 主题数量
n_top_words = 5  # 每个主题的主题词数量
pattern = '[\\s\\d,.<>/?:;\'\"[\\]{}()\\|~!\t"@#$%^&*\\-_=+，。\n《》、？：；""''｛｝【】（）…￥！—┄－]+'

def lda_analyze(request):
    spot_name = request.GET.get('name')
    print(spot_name)
    conn = pymysql.connect(host='60.215.128.117', port=15320, user='root', passwd='kissme77',
                           db='hx_cultural_transmission_sys',charset='utf8')

    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    cursor.execute("SELECT spot_id FROM scenicspot WHERE spot_name=%s",(spot_name))
    spot_id = cursor.fetchone()['spot_id']
    print("id名称为",spot_id)
    
    sql_query = "SELECT content FROM user_comment_spot WHERE spot_id=%s"
    
    # 执行SQL，并返回收影响行数
    effect_row = cursor.execute(sql_query, (spot_id))
    comment_list =cursor.fetchall()
    # print(comment_list)

    data = {
     '回答内容': [comment['content'] for comment in comment_list]  # 假设评论存储在数据库的第一列
 }

    df = pd.DataFrame(data).drop_duplicates().rename(columns={
        '回答内容': 'text'
    })

    # 设置停用词集合
    stop_words_set = set(['你', '我'])
    # 去重、去缺失、分词
    df['cut'] = (
        df['text']
        .apply(lambda x: str(x))
        .apply(lambda x: re.sub(pattern, ' ', x))
        .apply(lambda x: " ".join([word for word in jieba.lcut(x) if word not in stop_words_set]))
    )

    # 构造 tf-idf
    tf_idf_vectorizer = TfidfVectorizer()
    tf_idf = tf_idf_vectorizer.fit_transform(df['cut'])

    lda = LatentDirichletAllocation(
        n_components=n_topics,
        max_iter=50,
        learning_method='online',
        learning_offset=50,
        random_state=0)

    # 使用 tf_idf 语料使用 lda 模型
    lda.fit(tf_idf)

    # 计算 n_top_words 个主题词
    top_words_df = top_words_data_frame(lda, tf_idf_vectorizer, n_top_words)
    top_words_df=top_words_data_frame(lda, tf_idf_vectorizer, n_top_words)
    top_words_array=top_words_df.values
    # print(top_words_array)
    json_data=[]
    for topic_words in top_words_array:
        json_item = process_comments(topic_words)
        json_data.append(json_item)
    # print(json_data)
    # 保存 n_top_words 个主题词到 csv 文件中
    # top_words_df.to_csv(top_words_csv_path, encoding='utf-8-sig', index=None)

    # 转 tf_idf 为数组，以便后面使用它来对文本主题概率分布进行计算
    X = tf_idf.toarray()
    def calculate_word_frequency(comments, topic_words):
        word_freq = {}
        for word in topic_words:
            word_freq[word] = sum(comment.count(word) for comment in comments)
        return word_freq

    

    def predict_to_data_frame(model: LatentDirichletAllocation, X: np.ndarray) -> pd.DataFrame:
        matrix = model.transform(X)
        columns = [f'P(topic {i+1})' for i in range(len(model.components_))]
        df = pd.DataFrame(matrix, columns=columns)
        return df

    # 计算完毕主题概率分布情况
    predict_df = predict_to_data_frame(lda, X)
    frequency_data = {}
    for topic_words in top_words_array:
        freq = calculate_word_frequency(df['text'].tolist(), topic_words)
        frequency_data.update(freq)

    # print(frequency_data)
    keys_list = list(frequency_data.keys())
    values_list = list(frequency_data.values())
    sentiments_json=process_comments(keys_list)
    # print(sentiments_json)
    data=sentiments_json
    sentiments_list=[result['sentiment'] for result in data]
    result=[]
    for key,value,sentiment in zip(keys_list,values_list,sentiments_list):
        result.append({'topic':key,'frequency':value,'sentiment':sentiment})
    # 保存文本主题概率分布到 csv 文件中
    # predict_df.to_csv(predict_topic_csv_path, encoding='utf-8-sig', index=None)
    
    return JsonResponse(result,safe=False)

def lda_analyze_literature(request):
    """对文学评论进行LDA主题分析"""
    try:
        liter_name = request.GET.get('name')
        if not liter_name:
            return JsonResponse({
                'status': 'error',
                'message': '文学作品名称不能为空'
            }, status=400)

        # 数据库连接
        conn = pymysql.connect(host='60.215.128.117', port=15320, user='root', passwd='kissme77',
                             db='hx_cultural_transmission_sys', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 获取文学作品ID
        cursor.execute("SELECT liter_id FROM literature WHERE liter_name=%s", (liter_name,))
        result = cursor.fetchone()
        if not result:
            return JsonResponse({
                'status': 'error',
                'message': f'未找到文学作品: {liter_name}'
            }, status=404)
        
        liter_id = result['liter_id']

        # 获取该文学作品的所有评论
        sql_query = "SELECT comment_text FROM user_comment_literature WHERE liter_id=%s"
        cursor.execute(sql_query, (liter_id,))
        comment_list = cursor.fetchall()

        if not comment_list:
            return JsonResponse([])

        # 准备数据
        data = {
            '评论内容': [comment['comment_text'] for comment in comment_list]
        }

        df = pd.DataFrame(data).drop_duplicates().rename(columns={
            '评论内容': 'text'
        })

        # 设置停用词
        stop_words_set = set(['你', '我'])
        
        # 文本预处理：去重、去缺失、分词
        df['cut'] = (
            df['text']
            .apply(lambda x: str(x))
            .apply(lambda x: re.sub(pattern, ' ', x))
            .apply(lambda x: " ".join([word for word in jieba.lcut(x) if word not in stop_words_set]))
        )

        # 构造 tf-idf
        tf_idf_vectorizer = TfidfVectorizer()
        tf_idf = tf_idf_vectorizer.fit_transform(df['cut'])

        # LDA 模型
        lda = LatentDirichletAllocation(
            n_components=n_topics,
            max_iter=50,
            learning_method='online',
            learning_offset=50,
            random_state=0
        )

        # 训练 LDA 模型
        lda.fit(tf_idf)

        # 获取主题词
        top_words_df = top_words_data_frame(lda, tf_idf_vectorizer, n_top_words)
        top_words_array = top_words_df.values

        # 对主题词进行情感分析
        json_data = []
        for topic_words in top_words_array:
            json_item = process_comments(topic_words)
            json_data.append(json_item)

        # 计算词频
        X = tf_idf.toarray()
        frequency_data = {}
        for topic_words in top_words_array:
            freq = calculate_word_frequency(df['text'].tolist(), topic_words)
            frequency_data.update(freq)

        # 准备返回结果
        keys_list = list(frequency_data.keys())
        values_list = list(frequency_data.values())
        sentiments_json = process_comments(keys_list)
        data = sentiments_json
        sentiments_list = [result['sentiment'] for result in data]
        
        result = []
        for key, value, sentiment in zip(keys_list, values_list, sentiments_list):
            result.append({
                'topic': key,
                'frequency': value,
                'sentiment': sentiment
            })
        
        return JsonResponse(result, safe=False)

    except Exception as e:
        logger.error(f"处理文学作品 {liter_name} 的主题分析时出错: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            
            
            

def lda_analyze_food(request):
    """对食品评论进行LDA主题分析"""
    try:
        food_name = request.GET.get('name')
        if not food_name:
            return JsonResponse({
                'status': 'error',
                'message': '食品名称不能为空'
            }, status=400)

        # 数据库连接
        conn = pymysql.connect(host='60.215.128.117', port=15320, user='root', passwd='kissme77',
                             db='hx_cultural_transmission_sys', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 获取文学作品ID
        cursor.execute("SELECT food_id FROM food WHERE food_name=%s", (food_name,))
        result = cursor.fetchone()
        if not result:
            return JsonResponse({
                'status': 'error',
                'message': f'未找到食品: {food_name}'
            }, status=404)
        
        food_id = result['food_id']

        # 获取该食品的所有评论
        sql_query = "SELECT comment_text FROM user_comment_food WHERE food_id=%s"
        cursor.execute(sql_query, (food_id,))
        comment_list = cursor.fetchall()

        if not comment_list:
            return JsonResponse([])

        # 准备数据
        data = {
            '评论内容': [comment['comment_text'] for comment in comment_list]
        }

        df = pd.DataFrame(data).drop_duplicates().rename(columns={
            '评论内容': 'text'
        })

        # 设置停用词
        stop_words_set = set(['你', '我'])
        
        # 文本预处理：去重、去缺失、分词
        df['cut'] = (
            df['text']
            .apply(lambda x: str(x))
            .apply(lambda x: re.sub(pattern, ' ', x))
            .apply(lambda x: " ".join([word for word in jieba.lcut(x) if word not in stop_words_set]))
        )

        # 构造 tf-idf
        tf_idf_vectorizer = TfidfVectorizer()
        tf_idf = tf_idf_vectorizer.fit_transform(df['cut'])

        # LDA 模型
        lda = LatentDirichletAllocation(
            n_components=n_topics,
            max_iter=50,
            learning_method='online',
            learning_offset=50,
            random_state=0
        )

        # 训练 LDA 模型
        lda.fit(tf_idf)

        # 获取主题词
        top_words_df = top_words_data_frame(lda, tf_idf_vectorizer, n_top_words)
        top_words_array = top_words_df.values

        # 对主题词进行情感分析
        json_data = []
        for topic_words in top_words_array:
            json_item = process_comments(topic_words)
            json_data.append(json_item)

        # 计算词频
        X = tf_idf.toarray()
        frequency_data = {}
        for topic_words in top_words_array:
            freq = calculate_word_frequency(df['text'].tolist(), topic_words)
            frequency_data.update(freq)

        # 准备返回结果
        keys_list = list(frequency_data.keys())
        values_list = list(frequency_data.values())
        sentiments_json = process_comments(keys_list)
        data = sentiments_json
        sentiments_list = [result['sentiment'] for result in data]
        
        result = []
        for key, value, sentiment in zip(keys_list, values_list, sentiments_list):
            result.append({
                'topic': key,
                'frequency': value,
                'sentiment': sentiment
            })
        
        return JsonResponse(result, safe=False)

    except Exception as e:
        logger.error(f"处理食品 {food_name} 的主题分析时出错: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            
def lda_analyze_folk(request):
    """对食品评论进行LDA主题分析"""
    try:
        folk_name = request.GET.get('name')
        if not folk_name:
            return JsonResponse({
                'status': 'error',
                'message': '非遗民俗名称不能为空'
            }, status=400)

        # 数据库连接
        conn = pymysql.connect(host='60.215.128.117', port=15320, user='root', passwd='kissme77',
                             db='hx_cultural_transmission_sys', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 获取文学作品ID
        cursor.execute("SELECT folk_id FROM folk WHERE folk_name=%s", (folk_name,))
        result = cursor.fetchone()
        if not result:
            return JsonResponse({
                'status': 'error',
                'message': f'未找到非遗民俗: {folk_name}'
            }, status=404)
        
        folk_id = result['folk_id']

        # 获取该食品的所有评论
        sql_query = "SELECT comment_text FROM user_comment_folk WHERE folk_id=%s"
        cursor.execute(sql_query, (folk_id,))
        comment_list = cursor.fetchall()

        if not comment_list:
            return JsonResponse([])

        # 准备数据
        data = {
            '评论内容': [comment['comment_text'] for comment in comment_list]
        }

        df = pd.DataFrame(data).drop_duplicates().rename(columns={
            '评论内容': 'text'
        })

        # 设置停用词
        stop_words_set = set(['你', '我'])
        
        # 文本预处理：去重、去缺失、分词
        df['cut'] = (
            df['text']
            .apply(lambda x: str(x))
            .apply(lambda x: re.sub(pattern, ' ', x))
            .apply(lambda x: " ".join([word for word in jieba.lcut(x) if word not in stop_words_set]))
        )

        # 构造 tf-idf
        tf_idf_vectorizer = TfidfVectorizer()
        tf_idf = tf_idf_vectorizer.fit_transform(df['cut'])

        # LDA 模型
        lda = LatentDirichletAllocation(
            n_components=n_topics,
            max_iter=50,
            learning_method='online',
            learning_offset=50,
            random_state=0
        )

        # 训练 LDA 模型
        lda.fit(tf_idf)

        # 获取主题词
        top_words_df = top_words_data_frame(lda, tf_idf_vectorizer, n_top_words)
        top_words_array = top_words_df.values

        # 对主题词进行情感分析
        json_data = []
        for topic_words in top_words_array:
            json_item = process_comments(topic_words)
            json_data.append(json_item)

        # 计算词频
        X = tf_idf.toarray()
        frequency_data = {}
        for topic_words in top_words_array:
            freq = calculate_word_frequency(df['text'].tolist(), topic_words)
            frequency_data.update(freq)

        # 准备返回结果
        keys_list = list(frequency_data.keys())
        values_list = list(frequency_data.values())
        sentiments_json = process_comments(keys_list)
        data = sentiments_json
        sentiments_list = [result['sentiment'] for result in data]
        
        result = []
        for key, value, sentiment in zip(keys_list, values_list, sentiments_list):
            result.append({
                'topic': key,
                'frequency': value,
                'sentiment': sentiment
            })
        
        return JsonResponse(result, safe=False)

    except Exception as e:
        logger.error(f"处理非遗民俗 {folk_name} 的主题分析时出错: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()