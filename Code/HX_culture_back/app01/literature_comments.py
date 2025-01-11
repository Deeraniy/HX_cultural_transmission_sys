from django.http import JsonResponse
import pymysql
import logging

# 配置日志
logger = logging.getLogger(__name__)

def get_comment_list_literature(request):
    liter_name = request.GET.get('name')
    
    # 创建连接
    conn = pymysql.connect(
        host='120.233.26.237', 
        port=15320, 
        user='root', 
        passwd='kissme77',
        db='hx_cultural_transmission_sys',
        charset='utf8'
    )
    
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    
    # 查询liter_id
    cursor.execute("SELECT liter_id FROM literature WHERE liter_name=%s", (liter_name,))
    liter_result = cursor.fetchone()
    
    if liter_result:
        liter_id = liter_result['liter_id']
        logger.info(f"查到的liter_id: {liter_id}")
    else:
        logger.error(f"未找到文学作品: {liter_name}")
        cursor.close()
        conn.close()
        return JsonResponse({"message": "未找到文学作品"}, status=404)
    
    # 查询评论，获取所有相关字段
    sql_query = """
        SELECT 
            id, user_id, ip_location, comment_id, comment_text AS content, 
            like_count, liter_id AS spot_id, create_time, sentiment, 
            sentiment_confidence, platform 
        FROM user_comment_literature 
        WHERE liter_id=%s
    """
    cursor.execute(sql_query, (liter_id,))
    comment_list = cursor.fetchall()
    
    # 确保返回的格式与get_comment_list一致
    formatted_comments = [
        {
            'id': comment['id'],
            'user_id': comment['user_id'],
            'ip_location': comment['ip_location'],
            'comment_id': comment['comment_id'],
            'content': comment['content'],
            'like_count': comment['like_count'],
            'spot_id': comment['spot_id'],  # liter_id作为spot_id
            'create_time': comment['create_time'],
            'sentiment': comment['sentiment'],
            'sentiment_confidence': str(comment['sentiment_confidence']),  # 转换为字符串
            'platform': comment['platform']
        }
        for comment in comment_list
    ]
    
    logger.info(f"查到的评论数: {len(formatted_comments)}")
    
    # 关闭游标和连接
    cursor.close()
    conn.close()
    
    return JsonResponse({"comments": formatted_comments}) 