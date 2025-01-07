from datasets import load_dataset
import json
import os
import pandas as pd
from tqdm import tqdm

def get_instruction():
    instruction = "你是社交媒体评论情感分析的专家，请你判断以下评论的情感倾向。如果是正向的，请回答2，如果是中性的，请回答1，如果是负向的，请回答0。"
    return instruction

def get_input(sentence):
    input = f'评论内容：{sentence}'
    return input

def get_product_review_training_data():
    # 加载数据集
    ds = load_dataset("tyqiangz/multilingual-sentiments", "all")
    
    # 转换为DataFrame
    train_df = pd.DataFrame(ds['train'])
    
    # 创建用于保存的数据列表
    json_list = []
    instruction = get_instruction()
    
    # 处理每一行数据
    for _, row in tqdm(train_df.iterrows(), total=len(train_df), desc="处理数据"):
        # 检查文本是否为空或无效
        if not isinstance(row['text'], str) or len(row['text'].strip()) == 0:
            continue
            
        json_dict = {}
        json_dict['instruction'] = instruction
        json_dict['input'] = get_input(row['text'].strip())  # 去除首尾空格
        json_dict['output'] = str(row['label'])
        json_list.append(json_dict)
    
    # 转换为DataFrame并保存
    result_df = pd.DataFrame(json_list)
    
    # 创建data目录（如果不存在）
    os.makedirs('./data', exist_ok=True)
    
    # 保存为JSON格式
    result_df.to_json('./data/training.json', orient='records', lines=True, force_ascii=False)
    
    # 保存为CSV格式，确保使用UTF-8编码
    result_df.to_csv('./data/training.csv', index=False, encoding='utf-8')
    
    # 打印数据集信息和示例
    print("\n处理后的数据集大小：", len(result_df))
    print("\n标签分布：")
    print(result_df['output'].value_counts())
    print("\n示例数据（前5条）：")
    for _, row in result_df.head().iterrows():
        print("\n---")
        print("Input:", row['input'])
        print("Output:", row['output'])
    
    return result_df

# 执行函数
df = get_product_review_training_data()