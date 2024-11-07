# from zhipuai import ZhipuAI
# client = ZhipuAI(api_key="1af4f35363ea97ed269ee3099c04f7f3.3AGroi22UtegCtjf")  # 请替换为您的真实API密钥

# def generate_report(data):
#     monthly_stats = {}
#     for entry in data:
#         year = entry['year']
#         month = entry['month']
#         sentiment = entry['sentiment']
#         sentiment_score = entry['sentiment_score']
#         comment_count = entry['comment_count']
#         # 使用 (year, month) 作为键
#     key = (year, month)
#     if key not in monthly_stats:
#         # 初始化该月份的统计信息
#         monthly_stats[key] = {
#             'total_comments': 0,
#             'sentiment_counts': {'positive': 0, 'neutral': 0, 'negative': 0},
#             'sentiment_scores': {'positive': [], 'neutral': [], 'negative': []},
#         }
#     # 更新统计信息
#     monthly_stats[key]['total_comments'] += comment_count
#     monthly_stats[key]['sentiment_counts'][sentiment] += comment_count
#     monthly_stats[key]['sentiment_scores'][sentiment].append(sentiment_score * comment_count)  # 加权求和

# # 计算百分比和平均情感得分
# for key in monthly_stats:
#     stats = monthly_stats[key]
#     total_comments = stats['total_comments']
#     for sentiment in ['positive', 'neutral', 'negative']:
#         count = stats['sentiment_counts'][sentiment]
#         percentage = (count / total_comments) * 100 if total_comments > 0 else 0
#         # 计算平均情感得分
#         total_score = sum(stats['sentiment_scores'][sentiment])
#         avg_score = (total_score / count) if count > 0 else 0
#         stats['sentiment_counts'][sentiment] = {'count': count, 'percentage': percentage}
#         stats['sentiment_scores'][sentiment] = avg_score

# # 构建提示语
# prompt = "我已经完成了情感分析，分析结果如下：\n\n"
# for key in sorted(monthly_stats.keys()):
#     year, month = key
#     stats = monthly_stats[key]
#     prompt += f"{year}年{month}月:\n"
#     total_comments = stats['total_comments']
#     prompt += f"- 总评论数：{total_comments}\n"
#     for sentiment in ['positive', 'neutral', 'negative']:
#         count_info = stats['sentiment_counts'][sentiment]
#         avg_score = stats['sentiment_scores'][sentiment]
#         sentiment_chinese = {'positive': '正面', 'neutral': '中性', 'negative': '负面'}[sentiment]
#         # 仅在评论数大于0时添加描述
#         if count_info['count'] > 0:
#             if count_info['percentage'] == 100:
#                 prompt += f"  - {sentiment_chinese}评论占比居多\n"
#             else:
#                 prompt += f"  - {sentiment_chinese}反馈：{count_info['count']}条，占比{count_info['percentage']:.2f}%\n"
#             prompt += f"    - 平均情感得分：{avg_score:.2f}\n"
#     prompt += "\n"

# # 修改提示语，要求使用幽默的语调，并不包括改进建议
# prompt += "请基于以上数据，帮助我生成一份情感分析报告，包括每个月的情感趋势和总体总结，使用幽默的语调。请不要包括改进建议。"

# # 调用 ZhipuAI 的聊天模型
# response = client.chat.completions.create(
#     model="chatglm_std",
#     messages=[
#         {"role": "user", "content": prompt}
#     ]
# )

# # 获取生成的报告文本
# report = response.choices[0].message.content.strip()
# return report