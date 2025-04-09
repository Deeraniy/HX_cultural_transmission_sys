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
    返回每个主题每月的不同情感评论数量，包含平台信息
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
            # SQL查询，按月份、平台和情感类型统计评论数量
            sql = f"""
                SELECT 
                    DATE_FORMAT(STR_TO_DATE(comment_time, '%Y-%m-%d %H:%i:%s'), '%Y-%m') as month,
                    platform,
                    sentiment,
                    COUNT(*) as count
                FROM {table_name}
                GROUP BY month, platform, sentiment
                ORDER BY month
            """
            
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            # 处理查询结果
            theme_data = {}
            for row in rows:
                try:
                    # 安全处理元组解包，避免索引错误
                    if len(row) >= 4:
                        month, platform, sentiment, count = row
                    else:
                        # 记录日志或处理不完整数据
                        print(f"警告: 数据行格式不正确，跳过: {row}")
                        continue
                    
                    # 检查month和sentiment是否为None或空
                    if not month or not sentiment:
                        continue
                    
                    if month not in theme_data:
                        theme_data[month] = {
                            'total': {
                                'positive': 0,
                                'neutral': 0,
                                'negative': 0
                            },
                            'platforms': {}
                        }
                    
                    # 添加平台信息，如果平台为空则设为"其他"
                    platform = platform if platform else "其他"
                    if platform not in theme_data[month]['platforms']:
                        theme_data[month]['platforms'][platform] = {
                            'positive': 0,
                            'neutral': 0,
                            'negative': 0
                        }
                    
                    # 记录数据，确保sentiment是有效的字符串并转换为小写
                    sentiment_lower = str(sentiment).lower()
                    # 确保sentiment_lower是positive, neutral或negative中的一个
                    if sentiment_lower not in ['positive', 'neutral', 'negative']:
                        sentiment_lower = 'neutral'  # 默认为中性
                    
                    theme_data[month]['platforms'][platform][sentiment_lower] = count
                    theme_data[month]['total'][sentiment_lower] += count
                except Exception as row_error:
                    print(f"处理行时出错: {row}, 错误: {str(row_error)}")
                    continue
            
            # 转换数据结构为列表格式
            monthly_data = []
            for month, data in theme_data.items():
                platforms_list = []
                for platform_name, sentiments in data['platforms'].items():
                    platforms_list.append({
                        'platform': platform_name,
                        'sentiments': sentiments
                    })
                    
                monthly_data.append({
                    'month': month,
                    'total_sentiments': data['total'],
                    'platforms': platforms_list
                })
            
            result[theme_name] = {
                'theme_name': theme_name,
                'monthly_data': monthly_data
            }
        
        return JsonResponse({
            'code': 200,
            'message': 'success',
            'data': result
        })
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"获取数据失败: {str(e)}\n{error_details}")
        return JsonResponse({
            'code': 500,
            'message': f'获取数据失败：{str(e)}'
        })
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def get_theme_ip_distribution(request):
    """
    获取四个主题的IP地区分布统计
    返回每个主题下各个地区的评论数量
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
            # SQL查询，统计各IP地区的评论数量
            sql = f"""
                SELECT 
                    CASE 
                        WHEN ip_location IS NULL OR ip_location = '' THEN '其他'
                        ELSE SUBSTRING_INDEX(ip_location, '省', 1)
                    END as province,
                    COUNT(*) as count
                FROM {table_name}
                GROUP BY province
                ORDER BY count DESC
            """
            
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            # 处理查询结果
            ip_distribution = {}
            for row in rows:
                province, count = row
                # 处理特殊情况（直辖市等）
                if '市' in province and '省' not in province:
                    province = province.replace('市', '')
                elif '自治区' in province:
                    province = province.replace('自治区', '')
                elif '特别行政区' in province:
                    province = province.replace('特别行政区', '')
                
                ip_distribution[province] = count
            
            result[theme_name] = {
                'theme_name': theme_name,
                'total_count': sum(ip_distribution.values()),
                'ip_distribution': [
                    {
                        'province': province,
                        'count': count
                    }
                    for province, count in ip_distribution.items()
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

def get_theme_short_comments(request):
    """
    从filtered_user_comment表中获取各主题的简短评论
    每个主题随机选择50条字数少于15字的评论
    """
    if request.method != 'GET':
        return JsonResponse({'code': 405, 'message': '仅支持GET请求'})
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)  # 使用字典游标
        
        # 首先从tag表获取theme_name和tag_id的对应关系
        theme_sql = """
            SELECT DISTINCT theme_name, tag_id
            FROM tag
            WHERE theme_name IN ('spot', 'literature', 'food', 'folk')
        """
        cursor.execute(theme_sql)
        theme_tags = cursor.fetchall()
        
        # 构建theme_name到tag_ids的映射
        theme_tag_map = {}
        for row in theme_tags:
            theme_name = row['theme_name']
            tag_id = row['tag_id']
            if theme_name not in theme_tag_map:
                theme_tag_map[theme_name] = []
            theme_tag_map[theme_name].append(tag_id)
        
        result = {}
        
        # 对每个主题进行查询
        for theme_name, tag_ids in theme_tag_map.items():
            # 将tag_ids列表转换为字符串，用于IN子句
            tag_ids_str = ','.join(str(tag_id) for tag_id in tag_ids)
            
            # SQL查询，获取指定主题的简短评论
            sql = f"""
                SELECT 
                    comment_id,
                    comment_text,
                    comment_time,
                    sentiment,
                    sentiment_confidence
                FROM filtered_user_comment 
                WHERE 
                    tag_id IN ({tag_ids_str})
                    AND LENGTH(comment_text) < 45  -- 假设一个汉字占3个字符，15字约等于45个字符
                ORDER BY RAND()
                LIMIT 50
            """
            
            cursor.execute(sql)
            comments = cursor.fetchall()
            
            # 处理查询结果
            result[theme_name] = {
                'theme_name': theme_name,
                'comment_count': len(comments),
                'comments': [
                    {
                        'id': comment['comment_id'],
                        'text': comment['comment_text'],
                        'time': comment['comment_time'],
                        'sentiment': comment['sentiment'],
                        'confidence': float(comment['sentiment_confidence']) if comment['sentiment_confidence'] else None
                    }
                    for comment in comments
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

def get_theme_platform_distribution(request):
    """
    获取四个主题的平台评论分布统计
    返回每个主题下各个平台的评论数量和占比
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
            # SQL查询，统计各平台的评论数量
            sql = f"""
                SELECT 
                    CASE 
                        WHEN platform IS NULL OR platform = '' THEN '其他'
                        ELSE platform
                    END as platform_name,
                    COUNT(*) as count
                FROM {table_name}
                GROUP BY platform_name
                ORDER BY count DESC
            """
            
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            # 处理查询结果
            platform_distribution = []
            total_count = 0
            
            for row in rows:
                platform_name, count = row
                platform_distribution.append({
                    'platform': platform_name,
                    'count': count
                })
                total_count += count
            
            # 计算各平台占比
            for platform in platform_distribution:
                platform['percentage'] = round((platform['count'] / total_count) * 100, 2) if total_count > 0 else 0
            
            result[theme_name] = {
                'theme_name': theme_name,
                'total_count': total_count,
                'platform_distribution': platform_distribution
            }
        
        return JsonResponse({
            'code': 200,
            'message': 'success',
            'data': result
        })
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"获取平台分布数据失败: {str(e)}\n{error_details}")
        return JsonResponse({
            'code': 500,
            'message': f'获取数据失败：{str(e)}'
        })
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
