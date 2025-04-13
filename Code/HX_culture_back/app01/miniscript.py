import os
import re

# 设置图片文件夹路径
folder_path = 'D:/spring_boot_content/HX_cultural_sys/Code/vue/src/assets/Red'

# 获取该文件夹下的所有文件
def generate_imports(folder_path):
    # 获取文件夹下的所有文件，并筛选出图片文件（假设是 .jpg 格式）
    image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
    
    # 生成导入语句
    imports = []
    for image_file in image_files:
        # 提取文件名，不带扩展名
        image_name = os.path.splitext(image_file)[0]
        
        # 过滤掉包含特殊符号的文件名，允许中文字符
        if re.match(r'^[\w\u4e00-\u9fa5]+$', image_name):  # 允许字母、数字、下划线、中文
            import_statement = f"'{image_name}':{image_name}图片,"
            imports.append(import_statement)
    
    # 将导入语句写入到一个文件中
    output_file = 'imports.py'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(imports))
    
    print(f'导入语句已生成：{output_file}')

# 运行函数
generate_imports(folder_path)
