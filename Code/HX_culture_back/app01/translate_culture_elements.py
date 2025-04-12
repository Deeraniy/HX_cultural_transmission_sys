import json
from googletrans import Translator
import time
import os

def translate_culture_elements():
    # 初始化翻译器
    translator = Translator()
    
    # 读取原始JSON文件
    with open('culture_elements.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_items = len(data)
    print(f"开始翻译，共 {total_items} 条记录")
    
    # 检查是否存在已翻译的文件
    temp_file = 'culture_elements_temp.json'
    if os.path.exists(temp_file):
        with open(temp_file, 'r', encoding='utf-8') as f:
            translated_data = json.load(f)
            # 更新data中已翻译的部分
            for i, item in enumerate(data):
                if i < len(translated_data):
                    if 'title-en' in translated_data[i]:
                        item['title-en'] = translated_data[i]['title-en']
                    if 'description-en' in translated_data[i]:
                        item['description-en'] = translated_data[i]['description-en']
        print("已加载之前的翻译进度")
    
    # 遍历每个元素进行翻译
    for i, item in enumerate(data, 1):
        # 如果已经翻译过，跳过
        if 'title-en' in item and 'description-en' in item:
            continue
            
        try:
            # 翻译标题
            if item['title'] and 'title-en' not in item:
                title_translation = translator.translate(item['title'], dest='en')
                item['title-en'] = title_translation.text
            
            # 翻译描述
            if item['description'] and 'description-en' not in item:
                description_translation = translator.translate(item['description'], dest='en')
                item['description-en'] = description_translation.text
            
            # 打印进度
            if i % 10 == 0:
                print(f"已翻译 {i}/{total_items} 条记录")
                # 每翻译10条记录保存一次
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            
            # 避免触发API限制，每翻译10条记录暂停1秒
            if i % 10 == 0:
                time.sleep(1)
                
        except Exception as e:
            print(f"翻译第 {i} 条记录时出错: {str(e)}")
            # 如果出错，添加空字符串作为翻译
            if 'title-en' not in item:
                item['title-en'] = ''
            if 'description-en' not in item:
                item['description-en'] = ''
            
            # 出错后暂停2秒再继续
            time.sleep(2)
            continue
    
    # 保存最终的翻译结果
    with open('culture_elements_translated.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 删除临时文件
    if os.path.exists(temp_file):
        os.remove(temp_file)
    
    print("翻译完成！结果已保存到 culture_elements_translated.json")

if __name__ == '__main__':
    translate_culture_elements() 