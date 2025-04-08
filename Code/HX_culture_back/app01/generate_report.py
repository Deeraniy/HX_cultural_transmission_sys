import pymysql
import logging
import json
import time
from zhipuai import ZhipuAI
from spot_sentiments_analyze import sentiments_result_total_count as spot_sentiments
from liter_sentiments_analyze import sentiments_result_total_count as liter_sentiments
from food_sentiments_analyze import sentiments_result_total_count as food_sentiments
from folk_sentiments_analyze import sentiments_result_total_count as folk_sentiments

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 初始化智谱AI客户端
client = ZhipuAI(api_key="1af4f35363ea97ed269ee3099c04f7f3.3AGroi22UtegCtjf")

def get_all_items():
    """获取所有需要生成报告的项目"""
    conn = pymysql.connect(
        host='8.148.26.99', 
        port=3306, 
        user='root',
        passwd='song', 
        db='hx_cultural_transmission_sys',
        charset='utf8'
    )
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    
    items = {
        'spot': [],
        'literature': [],
        'food': [],
        'folk': []
    }
    
    try:
        # 获取所有景点
        cursor.execute("SELECT spot_id, spot_name FROM spot")
        items['spot'] = cursor.fetchall()
        
        # 获取所有文学作品
        cursor.execute("SELECT liter_id, liter_name FROM literature")
        items['literature'] = cursor.fetchall()
        
        # 获取所有食品
        cursor.execute("SELECT food_id, food_name FROM food")
        items['food'] = cursor.fetchall()
        
        # 获取所有民俗
        cursor.execute("SELECT folk_id, folk_name FROM folk")
        items['folk'] = cursor.fetchall()
        
    except Exception as e:
        logger.error(f"获取项目列表时出错: {str(e)}")
    finally:
        cursor.close()
        conn.close()
        
    return items

def process_sentiment_data(sentiment_data):
    """处理情感分析数据，准备生成报告"""
    if not isinstance(sentiment_data, dict) or 'status' not in sentiment_data:
        logger.error(f"情感分析返回的数据格式不正确: {sentiment_data}")
        return None
        
    if sentiment_data['status'] != 'success' or 'data' not in sentiment_data:
        logger.warning(f"情感分析未成功或缺少数据: {sentiment_data.get('message', '无详细信息')}")
        return None
        
    data = sentiment_data['data']
    if not data: # 检查 data 是否为空列表
        logger.warning("情感分析数据为空列表")
        return None

    # 处理数据，计算每个月的统计信息
    monthly_stats = {}
    for entry in data:
        # 添加对 entry 结构的检查，防止 KeyError
        if not all(k in entry for k in ['year', 'month', 'sentiment', 'sentiment_score', 'comment_count']):
            logger.warning(f"情感数据条目格式不完整，跳过: {entry}")
            continue
            
        year = entry['year']
        month = entry['month']
        sentiment = entry['sentiment']
        sentiment_score = entry['sentiment_score']
        comment_count = entry['comment_count']
        
        key = (year, month)
        if key not in monthly_stats:
            monthly_stats[key] = {
                'total_comments': 0,
                'sentiment_counts': {'positive': 0, 'neutral': 0, 'negative': 0},
                'sentiment_scores': {'positive': [], 'neutral': [], 'negative': []},
            }
        
        # 确保 sentiment 值是预期的类型
        if sentiment not in monthly_stats[key]['sentiment_counts']:
             logger.warning(f"未知的 sentiment 类型 '{sentiment}'，跳过条目: {entry}")
             continue

        monthly_stats[key]['total_comments'] += comment_count
        monthly_stats[key]['sentiment_counts'][sentiment] += comment_count
        monthly_stats[key]['sentiment_scores'][sentiment].append(sentiment_score * comment_count)
    
    # 如果处理后 monthly_stats 为空，也返回 None
    if not monthly_stats:
        logger.warning("处理后的月度统计数据为空")
        return None

    # 计算百分比和平均情感得分
    for key in monthly_stats:
        stats = monthly_stats[key]
        total_comments = stats['total_comments']
        for sentiment in ['positive', 'neutral', 'negative']:
            count = stats['sentiment_counts'][sentiment]
            percentage = (count / total_comments) * 100 if total_comments > 0 else 0
            total_score = sum(stats['sentiment_scores'][sentiment])
            avg_score = (total_score / count) if count > 0 else 0
            stats['sentiment_counts'][sentiment] = {'count': count, 'percentage': percentage}
            stats['sentiment_scores'][sentiment] = avg_score
    
    # 构建提示语
    prompt = "我已经完成了情感分析，分析结果如下：\n\n"
    
    for key in sorted(monthly_stats.keys()):
        year, month = key
        stats = monthly_stats[key]
        prompt += f"{year}年{month}月:\n"
        total_comments = stats['total_comments']
        prompt += f"- 总评论数：{total_comments}\n"
        for sentiment in ['positive', 'neutral', 'negative']:
            count_info = stats['sentiment_counts'][sentiment]
            avg_score = stats['sentiment_scores'][sentiment]
            sentiment_chinese = {'positive': '正面', 'neutral': '中性', 'negative': '负面'}[sentiment]
            if count_info['count'] > 0:
                if count_info['percentage'] == 100:
                    prompt += f"  - {sentiment_chinese}评论占比居多\n"
                else:
                    prompt += f"  - {sentiment_chinese}反馈：{count_info['count']}条，占比{count_info['percentage']:.2f}%\n"
                prompt += f"    - 平均情感得分：{avg_score:.2f}\n"
        prompt += "\n"
    
    prompt += (
        "请基于以上数据，帮助我生成一份情感分析报告，包括每个月的情感趋势和总体总结，"
        "使用幽默的语调,并在报告中多使用emoji和颜文字请不要包括改进建议。"
        "请在总结部分详细分析整体情感趋势，深入探讨可能的原因和影响，多写一些内容。"
    )
    
    return prompt

def generate_and_save_report(item_name, item_type):
    """生成并保存报告"""
    logger.info(f"正在为 {item_type} {item_name} 生成报告")
    
    # 创建模拟请求对象
    class MockRequest:
        def __init__(self, name):
            self.GET = {}
            self.GET['name'] = name
            
    request = MockRequest(item_name)
    
    conn = None
    cursor = None
    tag_id = None # 初始化 tag_id

    try:
        conn = pymysql.connect(
            host='8.148.26.99', 
            port=3306, 
            user='root',
            passwd='song', 
            db='hx_cultural_transmission_sys',
            charset='utf8mb4', # 保持 utf8mb4 以支持 emoji，但需确保数据库支持
            connect_timeout=10,
            read_timeout=30,
            write_timeout=30
        )
        cursor = conn.cursor()
        
        # 检查是否已有报告
        cursor.execute(
            """
            SELECT r.tag_id, r.content 
            FROM report r 
            JOIN tag t ON r.tag_id = t.tag_id 
            WHERE t.tag_name = %s AND t.theme_name = %s
            """,
            (item_name, item_type)
        )
        existing_report = cursor.fetchone()
        if existing_report:
            tag_id = existing_report[0] # 获取已存在报告的 tag_id
            if existing_report[1] != "暂无数据支撑报告生成":
                logger.info(f"{item_type} {item_name} 已有有效报告，跳过生成")
                return True
            else:
                logger.info(f"{item_type} {item_name} 存在'暂无数据'报告，尝试重新生成")
        
        # 检查是否有评论数据
        # --- 修改开始 ---
        # 根据 item_type 确定正确的表名和字段名
        if item_type == 'literature':
            comment_table = "user_comment_literature"
            id_field = "liter_id"
            name_field = "liter_name"
        else:
            comment_table = f"user_comment_{item_type}"
            id_field = f"{item_type}_id"
            name_field = f"{item_type}_name"
        # --- 修改结束 ---
        
        # 先获取项目ID
        cursor.execute(f"SELECT {id_field} FROM {item_type} WHERE {name_field} = %s", (item_name,))
        item_result = cursor.fetchone()
        
        if not item_result:
            logger.error(f"未找到 {item_type}: {item_name}")
            # 即使找不到项目，也尝试记录一个"暂无数据"的报告（如果tag存在）
            if tag_id:
                 cursor.execute(
                    "INSERT INTO report (tag_id, content) VALUES (%s, %s) "
                    "ON DUPLICATE KEY UPDATE content = VALUES(content)",
                    (tag_id, "项目信息未找到")
                 )
                 conn.commit()
            return False # 返回 False 表示失败
            
        item_id = item_result[0]
        
        # 检查或创建 tag
        if not tag_id: # 只有在上面没有获取到 tag_id 时才查询或创建
            cursor.execute(
                "SELECT tag_id FROM tag WHERE tag_name = %s AND theme_name = %s",
                (item_name, item_type)
            )
            tag_result = cursor.fetchone()
            
            if tag_result:
                tag_id = tag_result[0]
            else:
                try:
                    cursor.execute(
                        "INSERT INTO tag (tag_name, theme_name, origin_id) VALUES (%s, %s, %s)",
                        (item_name, item_type, item_id)
                    )
                    conn.commit()
                    tag_id = cursor.lastrowid
                    logger.info(f"为 {item_type} {item_name} 创建了新的 tag, ID: {tag_id}")
                except pymysql.Error as e:
                    logger.error(f"创建 tag 时出错 ({item_type} {item_name}): {str(e)}")
                    conn.rollback() # 回滚插入操作
                    return False # 创建 tag 失败，无法继续

        # 检查评论数量
        cursor.execute(f"SELECT COUNT(*) FROM {comment_table} WHERE {id_field} = %s", (item_id,))
        comment_count = cursor.fetchone()[0]
            
        # 如果没有评论，保存"暂无数据"信息
        if comment_count == 0:
            logger.info(f"{item_type} {item_name} 暂无评论数据")
            if tag_id: # 确保 tag_id 存在
                cursor.execute(
                    "INSERT INTO report (tag_id, content) VALUES (%s, %s) "
                    "ON DUPLICATE KEY UPDATE content = VALUES(content)",
                    (tag_id, "暂无数据支撑报告生成")
                )
                conn.commit()
            return True # 认为处理成功，因为没有数据是正常情况
            
        # --- 开始调用情感分析 ---
        sentiment_data = None
        analysis_successful = False
        try:
            logger.info(f"开始为 {item_type} {item_name} 调用情感分析...")
            # 根据类型调用不同的函数
            if item_type == 'spot':
                sentiment_data = spot_sentiments(request)
            elif item_type == 'literature':
                sentiment_data = liter_sentiments(request)
            elif item_type == 'food':
                sentiment_data = food_sentiments(request)
            elif item_type == 'folk':
                sentiment_data = folk_sentiments(request)
            else:
                logger.error(f"未知的项目类型: {item_type}")
                # 更新报告状态为错误 (如果 tag_id 已知)
                if tag_id:
                    cursor.execute(
                        "INSERT INTO report (tag_id, content) VALUES (%s, %s) "
                        "ON DUPLICATE KEY UPDATE content = VALUES(content)",
                        (tag_id, "未知的项目类型")
                    )
                    conn.commit()
                return False # 返回 False 表示失败

            # 严格检查情感分析结果
            # 检查返回的是否是字典以及 status 是否为 success
            if not isinstance(sentiment_data, dict) or sentiment_data.get('status') != 'success':
                # 尝试获取更详细的错误信息
                error_msg = "未知错误"
                if isinstance(sentiment_data, dict):
                    error_msg = sentiment_data.get('message', '情感分析返回失败状态但无详细信息')
                elif isinstance(sentiment_data, str): # 处理直接返回字符串的情况
                    error_msg = f"情感分析直接返回错误字符串: {sentiment_data}"
                else:
                    error_msg = f"情感分析返回了非预期的类型: {type(sentiment_data)}"
                
                logger.error(f"情感分析失败 ({item_type} {item_name}): {error_msg}")
                # 更新报告状态为错误
                if tag_id:
                    cursor.execute(
                        "INSERT INTO report (tag_id, content) VALUES (%s, %s) "
                        "ON DUPLICATE KEY UPDATE content = VALUES(content)",
                        (tag_id, f"情感分析失败: {error_msg[:250]}") # 限制错误信息长度以防数据库溢出
                    )
                    conn.commit()
                return False # 返回 False 表示失败
            
            logger.info(f"情感分析成功 ({item_type} {item_name})")
            analysis_successful = True

        except Exception as e:
            # 捕获调用情感分析函数本身抛出的异常 (比如 Django 设置错误)
            logger.error(f"调用情感分析函数时发生异常 ({item_type} {item_name}): {str(e)}")
            # 更新报告状态为错误
            if tag_id:
                cursor.execute(
                    "INSERT INTO report (tag_id, content) VALUES (%s, %s) "
                    "ON DUPLICATE KEY UPDATE content = VALUES(content)",
                    (tag_id, f"情感分析异常: {str(e)[:250]}") # 限制长度
                )
                conn.commit()
            return False # 返回 False 表示失败
        # --- 情感分析结束 ---

        # 处理情感数据，生成提示语
        prompt = process_sentiment_data(sentiment_data)
        if not prompt:
            logger.warning(f"{item_type} {item_name} 情感数据处理后为空或格式错误，无法生成报告")
            if tag_id:
                cursor.execute(
                    "INSERT INTO report (tag_id, content) VALUES (%s, %s) "
                    "ON DUPLICATE KEY UPDATE content = VALUES(content)",
                    (tag_id, "情感数据处理失败或无有效数据")
                )
                conn.commit()
            return False # 返回 False 表示失败
        
        # --- 开始调用 AI 生成报告 ---
        report_content = None
        try:
            logger.info(f"开始为 {item_type} {item_name} 调用 AI 生成报告...")
            response = client.chat.completions.create(
                model="chatglm_std",
                messages=[{
                    "role": "user", 
                    "content": "请生成一份不含emoji的报告。" + prompt # 确保提示语正确
                }],
                timeout=60
            )
            report_content = response.choices[0].message.content.strip()
            logger.info(f"AI 报告生成成功 ({item_type} {item_name})")
            
        except Exception as e:
            logger.error(f"调用AI接口出错 ({item_type} {item_name}): {str(e)}")
            if tag_id:
                cursor.execute(
                    "INSERT INTO report (tag_id, content) VALUES (%s, %s) "
                    "ON DUPLICATE KEY UPDATE content = VALUES(content)",
                    (tag_id, f"AI接口调用失败: {str(e)}")
                )
                conn.commit()
            return False # 返回 False 表示失败
        # --- AI 生成报告结束 ---
        
        # --- 开始保存报告 ---
        try:
            if report_content and tag_id: # 确保有内容和 tag_id
                # 精准的特殊字符清理，保留emoji
                def minimal_clean_text(text):
                    if not text:
                        return ""
                    
                    # 只移除真正会导致数据库问题的字符
                    problematic_chars = {
                        '\u0000': '',   # NULL字符
                        '\u001a': '',   # SUB字符(CTRL+Z)
                        # 其他少数会导致MySQL存储问题的字符
                    }
                    
                    for char, replacement in problematic_chars.items():
                        text = text.replace(char, replacement)
                    
                    # 确保所有字符在MySQL utf8mb4支持的范围内
                    cleaned_text = ''
                    for char in text:
                        # MySQL utf8mb4 支持 4 字节 Unicode (最大 0x10FFFF)
                        if ord(char) <= 0x10FFFF:
                            cleaned_text += char
                        # 超出范围的字符直接忽略
                    
                    return cleaned_text
                
                # 应用最小限度的清理函数
                clean_content = minimal_clean_text(report_content)
                
                # 检查清理前后是否有变化
                if clean_content != report_content:
                    logger.warning(f"报告内容包含不支持的特殊字符，已最小限度清理 ({item_type} {item_name})")
                    logger.debug(f"清理前长度: {len(report_content)}, 清理后长度: {len(clean_content)}")

                cursor.execute(
                    "INSERT INTO report (tag_id, content) VALUES (%s, %s) "
                    "ON DUPLICATE KEY UPDATE content = VALUES(content)",
                    (tag_id, clean_content)
                )
                conn.commit()
                logger.info(f"已为 {item_type} {item_name} 生成并保存报告")
                return True # 最终成功
            else:
                 logger.error(f"无法保存报告，内容为空或 tag_id 未找到 ({item_type} {item_name})")
                 return False

        except pymysql.Error as e:
            logger.error(f"保存报告到数据库时出错 ({item_type} {item_name}): {str(e)}")
            conn.rollback() # 回滚保存操作
            # 可以在这里尝试再次清理或记录更详细的错误
            if tag_id:
                 cursor.execute(
                    "INSERT INTO report (tag_id, content) VALUES (%s, %s) "
                    "ON DUPLICATE KEY UPDATE content = VALUES(content)",
                    (tag_id, f"数据库保存失败: {str(e)}")
                 )
                 conn.commit()
            return False # 返回 False 表示失败
        # --- 保存报告结束 ---
        
    except pymysql.Error as db_err:
        # 捕获数据库连接或操作层面的错误
        logger.error(f"数据库操作出错 ({item_type} {item_name}): {str(db_err)}")
        if conn and conn.open: # 检查连接是否仍然打开
             conn.rollback() # 尝试回滚
        return False # 返回 False 表示失败
    except Exception as e:
        # 捕获其他未预料的异常
        logger.error(f"处理 {item_type} {item_name} 时发生未捕获异常: {str(e)}")
        if conn and conn.open:
             conn.rollback()
        return False # 返回 False 表示失败
    finally:
        # 确保游标和连接总是关闭
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            logger.debug(f"数据库连接已关闭 ({item_type} {item_name})")

def main():
    """主函数"""
    items = get_all_items()
    success_count = 0
    fail_count = 0

    for item_type, item_list in items.items():
        # --- 修改开始 ---
        # 根据 item_type 确定正确的名称键
        if item_type == 'literature':
            name_key = 'liter_name' 
        elif item_type == 'spot':
            name_key = 'spot_name'
        elif item_type == 'food':
            name_key = 'food_name'
        elif item_type == 'folk':
            name_key = 'folk_name'
        else:
            logger.error(f"未知的项目类型: {item_type}，无法确定名称键")
            continue # 跳过未知类型
        # --- 修改结束 ---
            
        logger.info(f"--- 开始处理 {item_type} ---")
        for item in item_list:
            # 检查 item 是否是字典以及 name_key 是否存在
            if not isinstance(item, dict) or name_key not in item:
                logger.error(f"处理 {item_type} 时遇到无效的项目数据: {item}")
                fail_count += 1
                continue # 跳过无效数据

            item_name = item[name_key]
            if generate_and_save_report(item_name, item_type):
                success_count += 1
            else:
                fail_count += 1
            time.sleep(1) # 保持延迟
        logger.info(f"--- {item_type} 处理完成 ---")

    logger.info(f"所有报告生成任务完成。成功: {success_count}, 失败: {fail_count}")

def generate_food_report():
    """单独生成食品报告"""
    food_items = get_all_items().get('food', [])
    for item in food_items:
        item_name = item.get('food_name')
        if item_name:
            generate_and_save_report(item_name, 'food')
            
def generate_literature_report():
    """单独生成文学作品报告"""
    literature_items = get_all_items().get('literature', [])
    for item in literature_items:
        item_name = item.get('liter_name')
        if item_name:
            generate_and_save_report(item_name, 'literature')

if __name__ == "__main__":
    generate_literature_report()