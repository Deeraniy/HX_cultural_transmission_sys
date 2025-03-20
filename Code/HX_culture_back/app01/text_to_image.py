from dashscope import ImageSynthesis
import dashscope
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
import os
from datetime import datetime
from django.conf import settings

# 配置 API key
dashscope.api_key = "sk-e184c1f6d2524d00a3eb1de084684530"

# 配置图片保存路径
SAVE_DIR = os.path.join(settings.MEDIA_ROOT, 'generated_images')
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def generate_image_prompt(data):
    """根据活动信息生成图片提示词"""
    event_name = data.get("eventName", "")
    event_type = data.get("eventType", "")
    tags = data.get("tags", [])
    
    # 根据活动类型选择场景描述
    scene_desc = ""
    if "非遗" in event_type or "非遗" in " ".join(tags):
        scene_desc = "传统工艺展示场景，充满文化气息"
    elif "展览" in event_type:
        scene_desc = "现代展览馆场景，光线明亮"
    elif "演出" in event_type or "表演" in event_type:
        scene_desc = "舞台表演场景，灯光效果"
    else:
        scene_desc = "文化活动场景，人群互动"

    # 组合提示词
    prompt = f"""
请生成一张富有艺术感的宣传海报，展现{event_name}活动的精彩瞬间。
场景：{scene_desc}
风格：中国传统元素与现代设计融合，色彩鲜明
要素：{'、'.join(tags)} 等文化元素自然融入
构图：主题突出，层次分明
整体效果：专业大气，突出文化传承与创新
"""
    return prompt.strip()

@require_http_methods(["POST"])
def generate_publicity_image(request):
    """处理生成宣传图片的请求"""
    try:
        data = json.loads(request.body)
        
        # 验证必要字段
        required_fields = ["eventName", "eventType"]
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'code': 400,
                    'message': f'缺少必要字段：{field}',
                    'data': None
                })

        # 生成提示词
        prompt = generate_image_prompt(data)
        
        # 调用图像生成
        rsp = ImageSynthesis.call(
            model="wanx2.1-t2i-turbo",
            prompt=prompt,
            n=1,
            size='1024*1024'
        )

        # 处理返回结果
        if rsp.status_code == 200:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_urls = []
            
            for idx, result in enumerate(rsp.output.results):
                # 下载图片
                img_response = requests.get(result.url)
                if img_response.status_code != 200:
                    continue
                
                # 生成文件名和路径
                file_name = f"publicity_{timestamp}_{idx}.png"
                file_path = os.path.join(SAVE_DIR, file_name)
                
                # 保存图片
                with open(file_path, 'wb') as f:
                    f.write(img_response.content)
                
                # 构建可访问的URL
                image_url = f"{settings.MEDIA_URL}generated_images/{file_name}"
                image_urls.append(image_url)

            return JsonResponse({
                'code': 200,
                'message': 'success',
                'data': {
                    'images': image_urls,
                    'prompt': prompt
                }
            })
        else:
            return JsonResponse({
                'code': 500,
                'message': f'图片生成失败: {rsp.message}',
                'data': None
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            'code': 400,
            'message': '无效的JSON格式',
            'data': None
        })
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'生成图片失败：{str(e)}',
            'data': None
        })