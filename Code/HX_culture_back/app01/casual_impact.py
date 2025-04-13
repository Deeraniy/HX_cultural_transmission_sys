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
        tag_name = request.GET.get('name', '').strip()
        if not tag_name:
            return JsonResponse({
                'status': 'error',
                'message': '标签名称不能为空'
            }, status=400)
            
        logger.info(f"正在查询标签: {tag_name}")
        
        # 数据库连接
        conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', 
                             passwd='song', db='hx_cultural_transmission_sys', 
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
        
        # 处理缺失值
        # 1. 对于连续性数据，使用前后值的平均值填充
        df['cpi'] = df['cpi'].interpolate(method='linear', limit_direction='both')
        df['investment'] = df['investment'].interpolate(method='linear', limit_direction='both')
        df['sales_rate'] = df['sales_rate'].interpolate(method='linear', limit_direction='both')
        
        # 2. 检查是否还有缺失值
        if df.isnull().any().any():
            print("\n=== 警告：填充后仍存在缺失值 ===")
            print(df.isnull().sum())
            # 如果开头或结尾有缺失值，使用最近的有效值填充
            df = df.fillna(method='bfill').fillna(method='ffill')
        
        # 打印调试信息
        print("\n=== 准备的因果推理数据（处理缺失值后）===")
        print(df.head())
        print("\n=== 数据形状 ===")
        print(f"行数: {len(df)}, 列数: {len(df.columns)}")
        print("\n=== 数据类型 ===")
        print(df.dtypes)
        print("\n=== 缺失值统计 ===")
        print(df.isnull().sum())
        
        # 确保 dates 是一个包含日期对象的列表
        dates = pd.date_range(start='2021-01-01', periods=len(df), freq='ME').to_pydatetime().tolist()
        
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
            
        # 找出情感数据的重大变化点
        sentiment_data = df['sentiment'].values
        change_point, change_value = find_significant_changes(sentiment_data)
        
        if change_point is None:
            return {'error': '未找到显著的变化点'}
            
        print(f"\n=== 找到的变化点 ===")
        print(f"位置: {change_point}")
        print(f"变化值: {change_value}")
        
        # 准备因果推理数据
        impact_data = pd.DataFrame({
            'y': df['sentiment'],  # 情感分析得分作为因变量
            'x1': df['cpi'],      # 经济指标作为协变量
            'x2': df['investment'],
            'x3': df['sales_rate']
        })
        
        print("\n=== 准备的因果推理数据 ===")
        print(impact_data.head())
        print("\n相关性矩阵:")
        print(impact_data.corr())
        
        # 运行因果推理
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
        
        # 获取反事实预测值
        counterfactual_predictions = {
            'dates': [],
            'actual_sentiment': [],
            'predicted_sentiment': [],
            'ci_lower': [],
            'ci_upper': []
        }
        
        # 遍历后干预期的数据
        post_start = change_point + 1
        for i in range(post_start, len(dates)):
            counterfactual_predictions['dates'].append({
                'year': dates[i].year,
                'month': dates[i].month
            })
            counterfactual_predictions['actual_sentiment'].append(float(ci.inferences['response'].iloc[i]))
            counterfactual_predictions['predicted_sentiment'].append(float(ci.inferences['point_pred'].iloc[i]))
            counterfactual_predictions['ci_lower'].append(float(ci.inferences['point_pred_lower'].iloc[i]))
            counterfactual_predictions['ci_upper'].append(float(ci.inferences['point_pred_upper'].iloc[i]))
        
        # 提取分析结果
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
1. 变化点信息:
   - 变化点位置: 第{change_point}个月
   - 变化点日期: {dates[change_point].year}年{dates[change_point].month}月
   - 变化幅度: {change_value:.3f}

2. 平均效应分析:
   - 实际情感得分平均值: {summary_data['average']['actual']:.3f}
   - 预测情感得分平均值: {summary_data['average']['predicted']:.3f}
   - 平均因果效应: {summary_data['average']['effect']:.3f}
   - 95%置信区间: [{summary_data['average']['ci_lower']:.3f}, {summary_data['average']['ci_upper']:.3f}]

3. 累积效应分析:
   - 实际累积情感得分: {summary_data['cumulative']['actual']:.3f}
   - 预测累积情感得分: {summary_data['cumulative']['predicted']:.3f}
   - 累积因果效应: {summary_data['cumulative']['effect']:.3f}
   - 95%置信区间: [{summary_data['cumulative']['ci_lower']:.3f}, {summary_data['cumulative']['ci_upper']:.3f}]

4. 相对效应:
   - 相对变化: {relative_effect:.1f}%

5. 结论:
   在经济指标变化后的期间，情感得分的实际值与预测值之间存在{abs(summary_data['average']['effect']):.3f}的差异。
   这表明经济变化{"产生了显著" if abs(relative_effect) > 10 else "产生了轻微" if abs(relative_effect) > 5 else "没有产生显著"}影响。
"""
        report_text_en=f"""1. Change Point Information:
   - Change Point Location: Month {change_point}
   - Change Point Date: {dates[change_point].year}-{dates[change_point].month}
   - Change Magnitude: {change_value:.3f}

2. Average Effect Analysis:
   - Actual Sentiment Score Average: {summary_data['average']['actual']:.3f}
   - Predicted Sentiment Score Average: {summary_data['average']['predicted']:.3f}
   - Average Causal Effect: {summary_data['average']['effect']:.3f}
   - 95% Confidence Interval: [{summary_data['average']['ci_lower']:.3f}, {summary_data['average']['ci_upper']:.3f}]

3. Cumulative Effect Analysis:
   - Actual Cumulative Sentiment Score: {summary_data['cumulative']['actual']:.3f}
   - Predicted Cumulative Sentiment Score: {summary_data['cumulative']['predicted']:.3f}
   - Cumulative Causal Effect: {summary_data['cumulative']['effect']:.3f}
   - 95% Confidence Interval: [{summary_data['cumulative']['ci_lower']:.3f}, {summary_data['cumulative']['ci_upper']:.3f}]

4. Relative Effect:
   - Relative Change: {relative_effect:.1f}%

5. Conclusion:
   During the period after the change in economic indicators, there is a difference of {abs(summary_data['average']['effect']):.3f} between the actual and predicted sentiment scores.
   This suggests that the economic change {"had a significant" if abs(relative_effect) > 10 else "had a slight" if abs(relative_effect) > 5 else "had no significant"} impact.
"""
        
        return {
            'change_point_info': {
                'index': int(change_point),
                'date': {
                    'year': dates[change_point].year,
                    'month': dates[change_point].month
                },
                'value': float(change_value)
            },
            'impact_summary': summary_data,
            'impact_report': report_text,
            'impact_report_en': report_text_en,
            'counterfactual_predictions': counterfactual_predictions
        }
        
    except Exception as e:
        logger.error(f"因果推理分析失败: {str(e)}")
        return {'error': f'因果推理分析失败: {str(e)}'}

def test_casual_impact():
    """测试因果推理功能"""
    try:
        # 数据库连接
        conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', 
                             passwd='song', db='hx_cultural_transmission_sys', 
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

