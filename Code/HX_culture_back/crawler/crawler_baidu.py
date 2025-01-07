import pymysql
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
import re

def crawl_and_update_literature():
    try:
        # 数据库连接部分保持不变
        conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                             db='hx_cultural_transmission_sys', charset='utf8')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        # 获取所有文献记录
        cursor.execute("SELECT id, description FROM literature WHERE text IS NULL")
        literature_list = cursor.fetchall()
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        for item in literature_list:
            if item['description']:
                try:
                    # 获取百度百科页面内容
                    response = requests.get(item['description'], headers=headers)
                    response.encoding = 'utf-8'
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # 提取简介内容
                    summary_div = soup.find('div', class_='lemmaSummary_aDCp0')
                    if summary_div:
                        # 找到所有带有text_QZdcK类的span
                        text_spans = summary_div.find_all('span', class_='text_QZdcK')
                        # 提取每个span的文本并连接
                        summary_text = ''.join(span.get_text() for span in text_spans)
                        # 去除类似[2]的引用标注
                        summary_text = re.sub(r'\[\d+\]', '', summary_text).strip()
                        
                        # 更新数据库
                        cursor.execute(
                            "UPDATE literature SET text = %s WHERE id = %s",
                            (summary_text, item['id'])
                        )
                        conn.commit()
                
                except Exception as e:
                    print(f"爬取URL {item['description']} 时出错: {str(e)}")
                    continue
        
        cursor.close()
        conn.close()
        
        return JsonResponse({
            'status': 'success',
            'message': '爬取完成'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })
