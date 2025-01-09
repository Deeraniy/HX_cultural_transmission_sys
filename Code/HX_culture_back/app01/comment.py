from django.shortcuts import render, redirect,HttpResponse
import pymysql
import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_comment_list(request):
    spot_name = request.GET.get('name')
    
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
    
    # 查询spot_id
    cursor.execute("SELECT spot_id FROM scenicspot WHERE spot_name=%s", (spot_name,))
    spot_result = cursor.fetchone()
    
    if spot_result:
        spot_id = spot_result['spot_id']
        logger.info(f"查到的spot_id: {spot_id}")
    else:
        logger.error(f"未找到景点: {spot_name}")
        cursor.close()
        conn.close()
        return HttpResponse("未找到景点", status=404)
    
    # 查询评论
    sql_query = "SELECT * FROM usercomment WHERE spot_id=%s"
    cursor.execute(sql_query, (spot_id,))
    comment_list = cursor.fetchall()
    
    logger.info(f"查到的评论数: {len(comment_list)}")
    
    # 关闭游标和连接
    cursor.close()
    conn.close()
    
    return HttpResponse(comment_list)

def get_comment_list_recent(request):
    # pass
    spot_name=request.GET.get('spot_name')
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    current_day = datetime.datetime.now().day
    # 创建连接
    conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                           db='hx_cultural_transmission_sys',charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("SELECT spot_id FROM scenicspot WHERE spot_name=%s",(spot_name))
    spot_id=cursor.fetchone()['spot_id']
    sql_query = "SELECT * FROM usercomment WHERE spot_id=%s AND YEAR(comment_time)=%s AND MONTH(comment_time)=%s"
    # 执行SQL，并返回收影响行数
    effect_row = cursor.execute(sql_query, (spot_id, current_year, current_month))
    comment_list =cursor.fetchall()
    print(comment_list)

    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return HttpResponse(comment_list)

def get_comment_time_span(request):
    spot_name = request.GET.get('spot_name')
    
    # 创建连接
    conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                           db='hx_cultural_transmission_sys', charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    
    # 查询该地点的评论时间范围
    sql_query = "SELECT MIN(comment_time) AS start_time, MAX(comment_time) AS end_time FROM usercomment WHERE spot_id=(SELECT spot_id FROM scenicspot WHERE spot_name=%s)"
    cursor.execute(sql_query, (spot_name,))
    time_span = cursor.fetchone()
    
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    
    if time_span['start_time'] and time_span['end_time']:
        return HttpResponse(f"评论时间跨度: 从 {time_span['start_time']} 到 {time_span['end_time']}")
    else:
        return HttpResponse("没有找到相关评论时间。")


def get_comment_ip_count(request):
    spot_name = request.GET.get('spot_name')
    
    # 创建连接
    conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                           db='hx_cultural_transmission_sys', charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    
    # 查询该地点评论的IP地址种类数量
    sql_query = "SELECT COUNT(DISTINCT ip_location) AS ip_count FROM usercomment WHERE spot_id=(SELECT spot_id FROM scenicspot WHERE spot_name=%s)"
    cursor.execute(sql_query, (spot_name,))
    ip_count = cursor.fetchone()
    
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    
    return HttpResponse(f"评论IP地址种类数量: {ip_count['ip_count'] if ip_count['ip_count'] is not None else 0}")

def get_average_score_by_bi_month(request):
    spot_name = request.GET.get('spot_name')
    
    # 创建连接
    conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                           db='hx_cultural_transmission_sys', charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    
    # 获取当前日期
    current_date = datetime.datetime.now()
    last_year_date = current_date - datetime.timedelta(days=365)

    # SQL 查询，根据每两个月分组计算平均得分
    sql_query = """
        SELECT 
            DATE_FORMAT(comment_time, '%%Y-%%m') AS period,  -- 双百分号
            AVG(like_count) AS average_score
        FROM 
            usercomment
        WHERE 
            spot_id = (SELECT spot_id FROM scenicspot WHERE spot_name = %s) 
            AND comment_time >= %s
        GROUP BY 
            DATE_FORMAT(comment_time, '%%Y-%%m')  -- 这里也是双百分号
        ORDER BY 
            period DESC
        LIMIT 6
    """

    
    cursor.execute(sql_query, (spot_name, last_year_date))
    average_scores = cursor.fetchall()
    
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    print(average_scores)
    return HttpResponse(average_scores)

def get_comment_count_last_12_months(request):
    spot_name = request.GET.get('spot_name')
    
    # 创建连接
    conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                           db='hx_cultural_transmission_sys', charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 获取当前日期的12个月前的日期
    current_date = datetime.datetime.now()
    last_year_date = current_date - datetime.timedelta(days=365)

    # SQL 查询，统计最近12个月每月的评论数量
    sql_query = """
        SELECT 
            DATE_FORMAT(comment_time, '%%Y-%%m') AS month,
            COUNT(*) AS comment_count
        FROM 
            usercomment
        WHERE 
            spot_id = (SELECT spot_id FROM scenicspot WHERE spot_name = %s)
            AND comment_time >= %s
        GROUP BY 
            DATE_FORMAT(comment_time, '%%Y-%%m')
        ORDER BY 
            month DESC
    """

    cursor.execute(sql_query, (spot_name, last_year_date))
    monthly_comment_counts = cursor.fetchall()
    
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    
    #格式化返回的结果
    response_data = ""
    for record in monthly_comment_counts:
        response_data += f"{record['month']} 的评论数: {record['comment_count']}<br>"

    return HttpResponse(response_data if response_data else "没有找到相关评论记录。")

