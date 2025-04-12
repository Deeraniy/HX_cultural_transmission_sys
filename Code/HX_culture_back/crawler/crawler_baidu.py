import pymysql
import time
import random
from playwright.sync_api import sync_playwright
import re

def crawl_and_update_spots():
    try:
        # 数据库连接
        conn = pymysql.connect(host='8.148.26.99', port=3306, user='root', passwd='song',
                             db='hx_cultural_transmission_sys', charset='utf8')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        # 获取所有景点记录
        cursor.execute("SELECT spot_id, description FROM spot WHERE text IS NULL or text = ''")
        spot_list = cursor.fetchall()
        
        print(f"找到 {len(spot_list)} 个需要爬取的景点")
        
        with sync_playwright() as p:
            # 启动浏览器，这里不使用无头模式，这样可以看到浏览器界面
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                viewport={'width': 1280, 'height': 800},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            )
            page = context.new_page()
            
            success_count = 0
            
            try:
                for item in spot_list:
                    print(f"\n正在处理景点ID: {item['spot_id']}, URL: {item['description']}")
                    if item['description']:
                        try:
                            # 确保URL是完整的
                            url = item['description']
                            if '?' in url:
                                url = url.split('?')[0]
                            
                            # 访问页面
                            page.goto(url)
                            
                            # 等待页面加载
                            page.wait_for_load_state('networkidle')
                            
                            # 检查是否需要验证
                            if page.locator("text=百度安全验证").count() > 0 or page.locator("text=百度用户登录").count() > 0:
                                print(f"景点 {item['spot_id']} 需要安全验证，请在浏览器中完成验证...")
                                # 等待用户手动验证完成
                                input("请在浏览器中完成验证后按回车继续...")
                            
                            # 获取内容
                            content = None
                            
                            # 定位summary模块，使用更宽松的选择器
                            summary_div = page.locator('div[class*="para"][class*="summary"][class*="MARK_MODULE"]')
                            if summary_div.count() > 0:
                                # 获取所有text_qs7xs元素的文本（包括带有其他class的元素）
                                text_elements = summary_div.locator('span[class*="text_qs7xs"]')
                                texts = []
                                for i in range(text_elements.count()):
                                    text = text_elements.nth(i).inner_text()
                                    if text and text.strip():
                                        texts.append(text.strip())
                                content = ''.join(texts)
                            
                            if content:
                                # 清理文本
                                content = re.sub(r'\[\d+\]', '', content)  # 移除引用标记
                                content = re.sub(r'\s+', ' ', content)     # 规范化空白字符
                                content = content.strip()
                                
                                print(f"获取到的文本内容: {content[:100]}...")
                                
                                # 更新数据库
                                cursor.execute(
                                    "UPDATE spot SET text = %s WHERE spot_id = %s",
                                    (content, item['spot_id'])
                                )
                                conn.commit()
                                success_count += 1
                                print(f"成功更新景点 {item['spot_id']} 的描述")
                            else:
                                print(f"未找到景点 {item['spot_id']} 的简介内容")
                        
                        except Exception as e:
                            print(f"爬取URL {item['description']} 时出错: {str(e)}")
                            continue
                        
                        # 随机延时2-4秒
                        time.sleep(random.uniform(2, 4))
            
            finally:
                # 关闭浏览器
                browser.close()
        
        cursor.close()
        conn.close()
        
        return {
            'status': 'success',
            'message': f'景点描述爬取完成，成功更新 {success_count} 个景点'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

def main():
    print("开始爬取景点百度百科内容...")
    print("注意：遇到验证码时会打开浏览器窗口，请手动完成验证。")
    result = crawl_and_update_spots()
    print(f"爬取结果：{result}")

if __name__ == "__main__":
    main()
