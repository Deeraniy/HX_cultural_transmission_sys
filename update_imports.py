import os
import re

def update_imports(directory: str, package_name: str = "HXCulture_DIalog"):
    """
    更新Python文件中的导入路径
    
    Args:
        directory: D:\spring_boot_content\HX_cultural_sys\Code\HX_culture_back\HXCulture_DIalog
        package_name: HXCulture_DIalog
    """
    # 需要添加前缀的本地模块列表
    local_modules = [
        "config", "env", "logger", "dao", "model", "web", "api",
        "lang_chain", "utils", "app", "views", "urls", "AI", "app01"
    ]
    
    # 编译正则表达式 - 匹配更多导入模式
    import_patterns = [
        # 匹配 from xxx.yyy import zzz 格式
        r'^from\s+(?!\.|\bHXCulture_DIalog\b)(' + '|'.join(local_modules) + r')(?:\.|$).*?\s+import\s+.*$',
        # 匹配 import xxx 格式
        r'^import\s+(?!HXCulture_DIalog\b)(' + '|'.join(local_modules) + r')(?:\s+|$)',
        # 匹配单独的 from env/config import xxx
        r'^from\s+(?:env|config)\s+import\s+.*$'
    ]
    
    combined_pattern = re.compile('|'.join(import_patterns), re.MULTILINE)
    
    def process_file(file_path: str):
        """处理单个文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 如果文件中没有需要修改的导入，直接返回
        if not combined_pattern.search(content):
            return
        
        # 修改导入语句
        def replace_import(match):
            line = match.group(0)
            # 跳过已经有正确前缀的导入
            if package_name in line:
                return line
            # 跳过相对导入
            if line.startswith('from .'):
                return line
            if line.startswith('from '):
                # 处理 from env/config import xxx 的特殊情况
                if line.startswith('from env ') or line.startswith('from config '):
                    return f'from {package_name}.' + line[5:]
                return f'from {package_name}.' + line[5:]
            elif line.startswith('import '):
                return f'import {package_name}.' + line[7:]
            return line
        
        new_content = combined_pattern.sub(replace_import, content)
        
        # 如果内容有变化，写回文件
        if new_content != content:
            print(f"Updating {file_path}")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

    # 遍历目录
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    process_file(file_path)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    # 指定项目根目录
    project_dir = r"D:\spring_boot_content\HX_cultural_sys\Code\HX_culture_back"
    
    if not os.path.exists(project_dir):
        print(f"Error: Directory not found: {project_dir}")
        exit(1)
    
    print(f"Processing directory: {project_dir}")
    update_imports(project_dir)
    print("Done!") 