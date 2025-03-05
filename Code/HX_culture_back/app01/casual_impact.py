import pandas as pd
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import pymysql
import logging
from causalimpact import CausalImpact
import numpy as np
import json
import traceback
from django.conf import settings
import os

logger = logging.getLogger(__name__)

# 配置Django设置
def configure_django_settings():
    settings.configure(
        DEFAULT_CHARSET='utf-8',
        DEBUG=True,
        ALLOWED_HOSTS=['*'],
    )

# 修改日期解析逻辑
def parse_date_column(col_name):
    """解析Excel中的日期列名"""
    try:
        # 假设格式为 "2024年1月" 或类似格式
        parts = col_name.replace('年', '-').replace('月', '').split('-')
        year = int(parts[0])
        month = int(parts[1])
        return year, month
    except Exception as e:
        logger.error(f"解析日期失败: {col_name}, 错误: {str(e)}")
        return None, None

@require_GET
def sentiments_time_series(request):
    """根据标签名称获取情感分析时间序列结果"""
    try:
        # 读取经济数据
        file_path = 'app01/eco_data.xlsx'
        df = pd.read_excel(file_path)
        
        # 打印调试信息
        print("\n=== 经济数据 DataFrame 信息 ===")
        print(f"DataFrame 形状: {df.shape}")
        print(f"DataFrame 列名: {df.columns.tolist()}")
        
        # 初始化经济数据结果列表
        eco_results = []
        
        # 遍历每一列（日期）
        for col in df.columns[1:]:  # 跳过第一列（指标名称）
            year, month = parse_date_column(col)
            if year is None or month is None:
                continue
            
            # 创建该月份的数据字典
            month_data = {
                'year': year,
                'month': month,
                'cpi': None,  # 居民消费价格指数
                'investment': None,  # 固定资产投资完成额
                'sales_rate': None  # 工业产品销售率
            }
            
            # 获取各项指标的值
            try:
                cpi = df.loc[0, col]
                investment = df.loc[1, col]
                sales_rate = df.loc[2, col]
                
                # 打印调试信息
                print(f"列: {col}, CPI: {cpi}, Investment: {investment}, Sales Rate: {sales_rate}")
            except Exception as e:
                logger.error(f"访问数据时出错: {str(e)}")
                print(f"访问数据时出错: {str(e)}")
                continue
            
            # 只有当值不为空时才添加
            if pd.notna(cpi):
                month_data['cpi'] = float(cpi)
            if pd.notna(investment):
                month_data['investment'] = float(investment)
            if pd.notna(sales_rate):
                month_data['sales_rate'] = float(sales_rate)
            
            eco_results.append(month_data)
        
        # 按时间排序
        eco_results.sort(key=lambda x: (x['year'], x['month']))
        print(eco_results)
        # 原有的情感分析代码
        tag_name = request.GET.get('tag_name', '').strip()
        if not tag_name:
            return JsonResponse({
                'status': 'error',
                'message': '标签名称不能为空'
            }, status=400)
            
        logger.info(f"正在查询标签: {tag_name}")
        
        # 数据库连接
        conn = pymysql.connect(host='60.215.128.117', port=15320, user='root', 
                             passwd='kissme77', db='hx_cultural_transmission_sys', 
                             charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        
        # 获取 tag_id
        tag_sql = "SELECT tag_id FROM tag WHERE tag_name = %s LIMIT 1"
        cursor.execute(tag_sql, (tag_name,))
        tag_result = cursor.fetchone()
        
        if not tag_result:
            return JsonResponse({
                'status': 'error',
                'message': f'未找到标签: {tag_name}'
            }, status=404)
        
        tag_id = tag_result['tag_id']
        logger.info(f"找到标签ID: {tag_id}")
        
        # 查询评论数据
        comment_sql = """
            SELECT 
                sentiment, 
                sentiment_confidence, 
                SUBSTRING_INDEX(LEFT(comment_time, 7), '-', 1) as year,
                SUBSTRING_INDEX(LEFT(comment_time, 7), '-', -1) as month
            FROM user_comment 
            WHERE tag_id = %s AND sentiment IS NOT NULL
            ORDER BY comment_time
        """
        cursor.execute(comment_sql, (tag_id,))
        results = cursor.fetchall()
        
        if not results:
            return JsonResponse({
                'status': 'success',
                'data': [],
                'tag_info': {
                    'name': tag_name,
                    'id': tag_id
                },
                'message': '该标签暂无评论数据'
            })
        
        # 按年月分组数据
        monthly_data = {}
        for row in results:
            date_key = f"{row['year']}-{row['month']}"
            if date_key not in monthly_data:
                monthly_data[date_key] = []
            
            if row['sentiment'] and row['sentiment_confidence']:
                monthly_data[date_key].append(
                    (row['sentiment'], float(row['sentiment_confidence']))
                )
        
        # 计算每月的情感分析结果
        analysis_results = []
        for year_month, sentiments in monthly_data.items():
            year, month = map(int, year_month.split('-'))
            sentiment_score, dominant_sentiment = sentiment_month_analyze(sentiments)
            
            analysis_results.append({
                'year': year,
                'month': month,
                'sentiment_score': round(sentiment_score, 3),
                'sentiment': dominant_sentiment,
                'comment_count': len(sentiments)
            })
        
        # 按时间排序
        analysis_results.sort(key=lambda x: (x['year'], x['month']))
        
        # 在获取完所有数据后，执行因果推理分析
        casual_impact_results = perform_casual_impact_analysis(eco_results, analysis_results)
        
        # 修改返回结果，加入因果推理结果
        return JsonResponse({
            'status': 'success',
            'sentiment_data': analysis_results,
            'economic_data': eco_results,
            'casual_impact_analysis': casual_impact_results,
            'tag_info': {
                'name': tag_name,
                'id': tag_id
            }
        })
        
    except Exception as e:
        logger.error(f"处理数据时出错: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def find_significant_changes(data_list):
    """找出数据中的重大变化点"""
    if len(data_list) < 12:  # 至少需要12个点才能进行分析
        return None, None
    
    changes = []
    for i in range(3, len(data_list) - 3):  # 确保前后至少有3个点
        # 计算前后的平均值
        pre_mean = np.mean(data_list[i-3:i])
        post_mean = np.mean(data_list[i:i+3])
        # 计算变化幅度
        change = abs(post_mean - pre_mean)
        changes.append((i, change))
    
    if not changes:
        return None, None
    
    # 按变化幅度排序
    sorted_changes = sorted(changes, key=lambda x: x[1], reverse=True)
    return sorted_changes[0]

def prepare_casual_impact_data(eco_results, analysis_results):
    """准备因果推理所需的数据"""
    try:
        # 找出两个数据集的时间范围交集
        eco_dates = set((d['year'], d['month']) for d in eco_results)
        sentiment_dates = set((d['year'], d['month']) for d in analysis_results)
        common_dates = sorted(list(eco_dates.intersection(sentiment_dates)))
        
        if not common_dates:
            return None, None
        
        # 创建时间序列数据框
        data = {
            'sentiment': [],
            'cpi': [],
            'investment': [],
            'sales_rate': []
        }
        
        for year, month in common_dates:
            # 获取情感得分
            sentiment = next((d['sentiment_score'] for d in analysis_results 
                            if d['year'] == year and d['month'] == month), np.nan)
            # 获取经济数据
            eco_data = next((d for d in eco_results 
                            if d['year'] == year and d['month'] == month), None)
            
            data['sentiment'].append(sentiment)
            data['cpi'].append(eco_data['cpi'] if eco_data and eco_data['cpi'] is not None else np.nan)
            data['investment'].append(eco_data['investment'] if eco_data and eco_data['investment'] is not None else np.nan)
            data['sales_rate'].append(eco_data['sales_rate'] if eco_data and eco_data['sales_rate'] is not None else np.nan)
        
        df = pd.DataFrame(data)
        
        # 打印调试信息
        print("\n=== 准备的因果推理数据 ===")
        print(df)
        print("\n=== 数据形状 ===")
        print(f"行数: {len(df)}, 列数: {len(df.columns)}")
        print("\n=== 数据类型 ===")
        print(df.dtypes)
        print("\n=== 缺失值统计 ===")
        print(df.isnull().sum())
        
        # 确保 dates 是一个包含日期对象的列表
        dates = pd.date_range(start='2021-01-01', periods=len(df), freq='M').to_pydatetime().tolist()
        
        return df, dates
        
    except Exception as e:
        logger.error(f"准备因果推理数据时出错: {str(e)}")
        traceback.print_exc()
        return None, None


def perform_casual_impact_analysis(eco_results, analysis_results):
    """执行因果推理分析"""
    try:
        # 准备数据
        df, dates = prepare_casual_impact_data(eco_results, analysis_results)
        
        if df is None or dates is None:
            return {'error': '准备数据时出错'}
        
        if len(df) < 6:
            return {'error': '数据点不足以进行因果推理分析（至少需要6个点）'}
        
        # 对每个经济指标进行分析
        indicators = ['cpi', 'investment', 'sales_rate']
        results = {}
        
        for indicator in indicators:
            try:
                # 修改：创建 CausalImpact 对象，不使用日期索引
                impact_data = pd.DataFrame({
                    'y': df[indicator],
                    'x1': df['sentiment'],
                    'x2': df['investment'] if indicator != 'investment' else df['cpi'],
                    'x3': df['sales_rate'] if indicator != 'sales_rate' else df['cpi']
                })
                
                # 使用 ffill() 和 bfill() 替代 fillna(method='ffill')
                impact_data = impact_data.ffill().bfill()
                
                # 打印处理后的数据
                print(f"\n=== {indicator} 处理后数据 ===")
                print("DataFrame shape:", impact_data.shape)
                print("DataFrame head:")
                print(impact_data.head())
                
                if len(impact_data) < 6:
                    results[indicator] = {'error': f'{indicator} 的有效数据点不足（至少需要6个点）'}
                    continue
                
                # 找出该指标的重大变化点
                values = impact_data['y'].values
                change_point = len(values) // 2  # 使用数据中点作为变化点
                change_value = np.abs(np.mean(values[change_point:]) - np.mean(values[:change_point]))
                
                # 修改：创建 CausalImpact 对象，使用简单的数值索引
                ci = CausalImpact(
                    data=impact_data,
                    pre_period=[0, change_point],
                    post_period=[change_point + 1, len(impact_data) - 1],
                    model_args={
                        'niter': 1000,
                        'nseasons': 12,
                        'standardize': True
                    }
                )
                ci.run()
                
                # 打印完整的 inferences 信息
                print("\n=== Inferences DataFrame 完整信息 ===")
                print("列名:", ci.inferences.columns.tolist())
                print("\n前5行数据:")
                print(ci.inferences.head())
                print("\n数据类型:")
                print(ci.inferences.dtypes)
                
                # 使用正确的列名提取数据
                summary_data = {
                    'average': {
                        'actual': float(ci.inferences['response'].mean()),
                        'predicted': float(ci.inferences['point_pred'].mean()),
                        'effect': float(ci.inferences['point_effect'].mean()),
                        'ci_lower': float(ci.inferences['point_effect_lower'].mean()),
                        'ci_upper': float(ci.inferences['point_effect_upper'].mean())
                    },
                    'cumulative': {
                        'actual': float(ci.inferences['cum_response'].iloc[-1]),
                        'predicted': float(ci.inferences['cum_pred'].iloc[-1]),
                        'effect': float(ci.inferences['cum_effect'].iloc[-1]),
                        'ci_lower': float(ci.inferences['cum_effect_lower'].iloc[-1]),
                        'ci_upper': float(ci.inferences['cum_effect_upper'].iloc[-1])
                    }
                }
                
                # 计算相对效应
                relative_effect = (summary_data['cumulative']['effect'] / summary_data['cumulative']['actual']) * 100
                
                # 生成详细的报告文本
                report_text = f"""
因果推理分析报告 - {indicator}

1. 平均效应分析:
   - 实际平均值: {summary_data['average']['actual']:.2f}
   - 预测平均值: {summary_data['average']['predicted']:.2f}
   - 平均因果效应: {summary_data['average']['effect']:.2f}
   - 95%置信区间: [{summary_data['average']['ci_lower']:.2f}, {summary_data['average']['ci_upper']:.2f}]

2. 累积效应分析:
   - 实际累积值: {summary_data['cumulative']['actual']:.2f}
   - 预测累积值: {summary_data['cumulative']['predicted']:.2f}
   - 累积因果效应: {summary_data['cumulative']['effect']:.2f}
   - 95%置信区间: [{summary_data['cumulative']['ci_lower']:.2f}, {summary_data['cumulative']['ci_upper']:.2f}]

3. 相对效应:
   - 相对变化: {relative_effect:.1f}%

4. 统计显著性:
   - 置信区间是否包含0: {"否" if summary_data['average']['ci_lower'] * summary_data['average']['ci_upper'] > 0 else "是"}
   - 效应方向: {"正向" if summary_data['average']['effect'] > 0 else "负向" if summary_data['average']['effect'] < 0 else "无显著效应"}

5. 结论:
   在干预后期间，{indicator}的实际值与预测值之间存在{abs(summary_data['average']['effect']):.2f}的差异。
   这表明干预{"产生了显著" if abs(relative_effect) > 10 else "产生了轻微" if abs(relative_effect) > 5 else "没有产生显著"}影响。
   累积来看，干预导致{indicator}{"增加" if summary_data['cumulative']['effect'] > 0 else "减少"}了{abs(summary_data['cumulative']['effect']):.2f}个单位。
"""
                
                results[indicator] = {
                    'change_point_index': int(change_point),
                    'change_point_date': {
                        'year': dates[change_point].year,
                        'month': dates[change_point].month
                    },
                    'change_value': float(change_value),
                    'pre_period_mean': float(impact_data['y'][:change_point].mean()),
                    'post_period_mean': float(impact_data['y'][change_point:].mean()),
                    'impact_summary': summary_data,
                    'impact_report': report_text
                }
            except Exception as e:
                logger.error(f"处理指标 {indicator} 时出错: {str(e)}")
                results[indicator] = {'error': f'处理数据时出错: {str(e)}'}
        
        return results
        
    except Exception as e:
        logger.error(f"因果推理分析整体失败: {str(e)}")
        return {'error': f'因果推理分析整体失败: {str(e)}'}

def create_mock_sentiment_data():
    """创建模拟的情感分析数据"""
    sentiment_data = []
    # 只创建2024-2025年的模拟数据，与经济数据时间范围匹配
    for year in range(2024, 2026):
        for month in range(1, 13):
            # 如果是2025年且月份超过1月，就停止
            if year == 2025 and month > 1:
                break
                
            sentiment_data.append({
                'year': year,
                'month': month,
                'sentiment_score': 0.75,  # 模拟情感分数
                'sentiment': 'positive',
                'comment_count': 50
            })
    return sentiment_data

def test_casual_impact():
    """测试因果推理功能"""
    try:
        # 数据库连接
        conn = pymysql.connect(host='60.215.128.117', port=15320, user='root', 
                             passwd='kissme77', db='hx_cultural_transmission_sys', 
                             charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        
        tag_name = "土家族竹雕"
        logger.info(f"正在查询标签: {tag_name}")
        
        # 获取 tag_id
        tag_sql = "SELECT tag_id FROM tag WHERE tag_name = %s LIMIT 1"
        cursor.execute(tag_sql, (tag_name,))
        tag_result = cursor.fetchone()
        
        if not tag_result:
            print(f"未找到标签: {tag_name}")
            return
        
        tag_id = tag_result['tag_id']
        logger.info(f"找到标签ID: {tag_id}")
        
        # 查询评论数据
        comment_sql = """
            SELECT 
                sentiment, 
                sentiment_confidence, 
                SUBSTRING_INDEX(LEFT(comment_time, 7), '-', 1) as year,
                SUBSTRING_INDEX(LEFT(comment_time, 7), '-', -1) as month
            FROM user_comment 
            WHERE tag_id = %s AND sentiment IS NOT NULL
            ORDER BY comment_time
        """
        cursor.execute(comment_sql, (tag_id,))
        results = cursor.fetchall()
        
        if not results:
            print("该标签暂无评论数据")
            return
        
        # 按年月分组数据
        monthly_data = {}
        for row in results:
            date_key = f"{row['year']}-{row['month']}"
            if date_key not in monthly_data:
                monthly_data[date_key] = []
            
            if row['sentiment'] and row['sentiment_confidence']:
                monthly_data[date_key].append(
                    (row['sentiment'], float(row['sentiment_confidence']))
                )
        
        # 计算每月的情感分析结果
        analysis_results = []
        for year_month, sentiments in monthly_data.items():
            year, month = map(int, year_month.split('-'))
            sentiment_score, dominant_sentiment = sentiment_month_analyze(sentiments)
            
            analysis_results.append({
                'year': year,
                'month': month,
                'sentiment_score': round(sentiment_score, 3),
                'sentiment': dominant_sentiment,
                'comment_count': len(sentiments)
            })
        
        # 按时间排序
        analysis_results.sort(key=lambda x: (x['year'], x['month']))
        
        # 获取经济数据
        file_path = 'app01/eco_data.xlsx'
        df = pd.read_excel(file_path)
        eco_results = []
        
        # 打印列名以进行调试
        print("\n=== Excel列名 ===")
        print(df.columns.tolist())
        
        # 遍历每一列（日期）
        for col in df.columns[1:]:  # 跳过第一列（指标名称）
            year, month = parse_date_column(col)
            if year is None or month is None:
                print(f"无法解析日期: {col}")
                continue
            
            print(f"成功解析日期: {year}年{month}月")
            
            month_data = {
                'year': year,
                'month': month,
                'cpi': None,
                'investment': None,
                'sales_rate': None
            }
            
            try:
                cpi = df.loc[0, col]
                investment = df.loc[1, col]
                sales_rate = df.loc[2, col]
                
                # 打印调试信息
                print(f"列: {col}, CPI: {cpi}, Investment: {investment}, Sales Rate: {sales_rate}")
            except Exception as e:
                logger.error(f"访问数据时出错: {str(e)}")
                print(f"访问数据时出错: {str(e)}")
                continue
            
            if pd.notna(cpi):
                month_data['cpi'] = float(cpi)
            if pd.notna(investment):
                month_data['investment'] = float(investment)
            if pd.notna(sales_rate):
                month_data['sales_rate'] = float(sales_rate)
            
            eco_results.append(month_data)
        
        # 按时间排序
        eco_results.sort(key=lambda x: (x['year'], x['month']))
        
        # 执行因果推理分析
        casual_impact_results = perform_casual_impact_analysis(eco_results, analysis_results)
        
        # 打印结果
        print("\n=== 情感分析结果 ===")
        print(json.dumps(analysis_results[:5], indent=2, ensure_ascii=False))
        
        print("\n=== 经济数据 ===")
        print(json.dumps(eco_results[:5], indent=2, ensure_ascii=False))
        
        # 将结果中的 numpy 数据类型转换为 Python 原生数据类型
        def convert_to_native(obj):
            if isinstance(obj, np.generic):
                return obj.item()
            raise TypeError
        
        print("\n=== 因果推理分析结果 ===")
        print(json.dumps(casual_impact_results, indent=2, ensure_ascii=False, default=convert_to_native))
            
    except Exception as e:
        print(f"测试过程中出错: {str(e)}")
        traceback.print_exc()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def sentiment_month_analyze(sentiments):
    """分析一个月的情感数据"""
    if not sentiments:
        return 0, 'neutral'
    
    total_score = 0
    total_weight = 0
    
    for sentiment, confidence in sentiments:
        # 将情感转换为分数
        if sentiment == 'positive':
            score = 1
        elif sentiment == 'negative':
            score = -1
        else:
            score = 0
            
        # 加权计算
        total_score += score * confidence
        total_weight += confidence
    
    # 计算加权平均分数
    if total_weight > 0:
        avg_score = total_score / total_weight
    else:
        avg_score = 0
    
    # 确定主导情感
    if avg_score > 0.1:
        dominant_sentiment = 'positive'
    elif avg_score < -0.1:
        dominant_sentiment = 'negative'
    else:
        dominant_sentiment = 'neutral'
    
    return avg_score, dominant_sentiment

if __name__ == "__main__":
    # 设置日志级别
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # 运行测试
    test_casual_impact()

