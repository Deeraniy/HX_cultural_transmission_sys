import json
from googletrans import Translator
import time
import os

def translate_data_and_links():
    # 初始化翻译器
    translator = Translator()
    
    # 读取原始JSON文件
    data_file_path = r'D:\spring_boot_content\HX_cultural_sys\Code\vue\static\data.json'  # 修改文件路径
    with open(data_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_items = len(data['data'])
    print(f"开始翻译，共 {total_items} 条记录")
    
    # 检查是否存在已翻译的文件
    temp_file = 'data_temp.json'
    if os.path.exists(temp_file):
        with open(temp_file, 'r', encoding='utf-8') as f:
            translated_data = json.load(f)
            # 更新data中已翻译的部分
            for i, item in enumerate(data['data']):
                if i < len(translated_data['data']):
                    if 'name-en' in translated_data['data'][i]:
                        item['name-en'] = translated_data['data'][i]['name-en']
        print("已加载之前的翻译进度")
    
    # 翻译data部分
    for i, item in enumerate(data['data'], 1):
        # 如果已经翻译过，跳过
        if 'name-en' in item:
            continue
            
        try:
            # 翻译名称
            if item['name'] and 'name-en' not in item:
                name_translation = translator.translate(item['name'], dest='en')
                item['name-en'] = name_translation.text
            
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
            if 'name-en' not in item:
                item['name-en'] = ''
            
            # 出错后暂停2秒再继续
            time.sleep(2)
            continue
    
    # 翻译links部分
    for i, link in enumerate(data['links'], 1):
        # 如果已经翻译过，跳过
        if 'name-en' in link:
            continue
            
        try:
            # 翻译连接名称
            if link['name'] and 'name-en' not in link:
                link_translation = translator.translate(link['name'], dest='en')
                link['name-en'] = link_translation.text
            
            # 打印进度
            if i % 10 == 0:
                print(f"已翻译 {i}/{len(data['links'])} 条链接记录")
                # 每翻译10条记录保存一次
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            
            # 避免触发API限制，每翻译10条记录暂停1秒
            if i % 10 == 0:
                time.sleep(1)
                
        except Exception as e:
            print(f"翻译第 {i} 条链接记录时出错: {str(e)}")
            # 如果出错，添加空字符串作为翻译
            if 'name-en' not in link:
                link['name-en'] = ''
            
            # 出错后暂停2秒再继续
            time.sleep(2)
            continue
    
    # 保存最终的翻译结果
    with open('data_translated.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 删除临时文件
    if os.path.exists(temp_file):
        os.remove(temp_file)
    
    print("翻译完成！结果已保存到 data_translated.json")

if __name__ == '__main__':
    translate_data_and_links()
