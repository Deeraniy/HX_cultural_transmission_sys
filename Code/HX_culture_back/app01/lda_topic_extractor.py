import numpy as np
import pandas as pd
import jieba
import re
import pymysql
from django.http import JsonResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

from app01.sentiments_analyze import process_comments



# 输出主题词的文件路径
top_words_csv_path = './top-topic-words.csv'
# 输出各文档所属主题的文件路径
predict_topic_csv_path = './document-distribution.csv'
# 选定的主题数
n_topics = 1
# 要输出的每个主题的前 n_top_words 个主题词数
n_top_words = 10
# 去除无意义字符的正则表达式
pattern = '[\\s\\d,.<>/?:;\'\"[\\]{}()\\|~!\t"@#$%^&*\\-_=+，。\n《》、？：；""''｛｝【】（）…￥！—┄－]+'

def lda_analyze(request):
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

    def top_words_data_frame(model: LatentDirichletAllocation, 
                            tf_idf_vectorizer: TfidfVectorizer, 
                            n_top_words: int) -> pd.DataFrame:
        rows = []
        feature_names = tf_idf_vectorizer.get_feature_names_out()
        for topic in model.components_:
            top_words = [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
            rows.append(top_words)
        columns = [f'topic word {i+1}' for i in range(n_top_words)]
        df = pd.DataFrame(rows, columns=columns)

        return df

    # 计算 n_top_words 个主题词
    top_words_df = top_words_data_frame(lda, tf_idf_vectorizer, n_top_words)
    top_words_df=top_words_data_frame(lda, tf_idf_vectorizer, n_top_words)
    top_words_array=top_words_df.values
    print(top_words_array)
    json_data=[]
    for topic_words in top_words_array:
        json_item = process_comments(topic_words)
        json_data.append(json_item)
    print(json_data)
    # 保存 n_top_words 个主题词到 csv 文件中
    # top_words_df.to_csv(top_words_csv_path, encoding='utf-8-sig', index=None)

    # 转 tf_idf 为数组，以便后面使用它来对文本主题概率分布进行计算
    X = tf_idf.toarray()

    def predict_to_data_frame(model: LatentDirichletAllocation, X: np.ndarray) -> pd.DataFrame:
        matrix = model.transform(X)
        columns = [f'P(topic {i+1})' for i in range(len(model.components_))]
        df = pd.DataFrame(matrix, columns=columns)
        return df

    # 计算完毕主题概率分布情况
    predict_df = predict_to_data_frame(lda, X)

    # 保存文本主题概率分布到 csv 文件中
    # predict_df.to_csv(predict_topic_csv_path, encoding='utf-8-sig', index=None)
    result={'topic_words':top_words_df.to_dict(orient='records')}
    return JsonResponse(json_data,safe=False)