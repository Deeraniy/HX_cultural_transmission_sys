from transformers import pipeline
import pandas as pd
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 初始化情感分析模型
distilled_student_sentiment_classifier = pipeline(
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", 
    return_all_scores=True
)

def get_sentiment_label(text):
    """获取文本的情感标签和得分"""
    try:
        results = distilled_student_sentiment_classifier(text)[0]  # 获取分析结果
        # 找出得分最高的标签
        max_score_label = max(results, key=lambda x: x['score'])
        return max_score_label['label'], max_score_label['score']
    except (ValueError, RuntimeError, TypeError) as e:
        logger.error("处理文本时出错: %s. 错误信息: %s", text, str(e))
        return 'error', 0.0

def process_comments(comments_list):
    """处理评论列表并返回带标签的DataFrame"""
    results = []
    for comment in comments_list:
        label, score = get_sentiment_label(comment)
        results.append({
            'comment': comment,
            'sentiment': label,
            'confidence': score
        })
    return pd.DataFrame(results)

# 使用示例
if __name__ == "__main__":
    # 示例评论列表
    comments = [
        "今天真是个好天气",
        "I love this movie and i would watch it again and again!",
        "这个产品质量太差了",
        "Service was just okay"
    ]
    
    # 处理评论
    results_df = process_comments(comments)
    logger.info("处理完成，结果如下：\n%s", results_df)