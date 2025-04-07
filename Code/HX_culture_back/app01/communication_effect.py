from django.http import JsonResponse
import pymysql
from datetime import datetime
import calendar

def get_db_connection():
    """获取数据库连接"""
    return pymysql.connect(
        host='8.148.26.99',
        port=3306,
        user='root',
        passwd='song',
        db='hx_cultural_transmission_sys',
        charset='utf8'
    )

def get_theme_comments_sentiment(request):
    """
    获取四个主题的评论情感分析数据
    返回每个主题每月的不同情感评论数量
    """
    if request.method != 'GET':
        return JsonResponse({'code': 405, 'message': '仅支持GET请求'})
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 定义要查询的表和对应的主题名
        tables = {
            'spot': 'user_comment_spot',
            'literature': 'user_comment_literature',
            'food': 'user_comment_food',
            'folk': 'user_comment_folk'
        }
        
        result = {}
        
        for theme_name, table_name in tables.items():
            # SQL查询，按月份和情感类型统计评论数量
            sql = f"""
                SELECT 
                    DATE_FORMAT(STR_TO_DATE(comment_time, '%Y-%m-%d %H:%i:%s'), '%Y-%m') as month,
                    sentiment,
                    COUNT(*) as count
                FROM {table_name}
                GROUP BY month, sentiment
                ORDER BY month
            """
            
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            # 处理查询结果
            theme_data = {}
            for row in rows:
                month, sentiment, count = row
                if month not in theme_data:
                    theme_data[month] = {
                        'positive': 0,
                        'neutral': 0,
                        'negative': 0
                    }
                theme_data[month][sentiment.lower()] = count
            
            result[theme_name] = {
                'theme_name': theme_name,
                'monthly_data': [
                    {
                        'month': month,
                        'sentiments': sentiments
                    }
                    for month, sentiments in theme_data.items()
                ]
            }
        
        return JsonResponse({
            'code': 200,
            'message': 'success',
            'data': result
        })
        
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'获取数据失败：{str(e)}'
        })
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
