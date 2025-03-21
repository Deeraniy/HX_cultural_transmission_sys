import os
from pathlib import Path
from dotenv import load_dotenv
from dashscope import ImageSynthesis
import dashscope
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
from http import HTTPStatus
import oss2
from IPython.display import Image as IPyImage, display
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
import time

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 加载 .env 文件
load_dotenv(os.path.join(BASE_DIR, '.env'))

# 检查环境变量是否加载成功
access_key_id = os.getenv("ACCESS_KEY_ID")
access_key_secret = os.getenv("ACCESS_KEY_SECRET")
dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")

if not all([access_key_id, access_key_secret, dashscope_api_key]):
    raise ValueError("环境变量未正确加载，请检查 .env 文件")

# 阿里云 OSS 配置
endpoint = 'http://oss-cn-wuhan-lr.aliyuncs.com'  # 使用武汉区域的 endpoint
bucket_name = 'hx-cultural-images'
oss_folder = 'text_to_graph'

# # 配置 API key
dashscope.api_key = dashscope_api_key

# 初始化 OSS bucket
def init_oss_bucket():
    try:
        auth = oss2.Auth(access_key_id, access_key_secret)
        # 配置 bucket
        bucket = oss2.Bucket(
            auth, 
            endpoint, 
            bucket_name,
            connect_timeout=60,
            is_cname=False,
            enable_crc=False
        )
        
        # 访问时使用的 URL（武汉区域）
        public_endpoint = 'hx-cultural-images.oss-cn-wuhan-lr.aliyuncs.com'
        
        return bucket, public_endpoint
    except Exception as e:
        print(f"初始化 OSS 失败: {str(e)}")
        raise e

try:
    # 初始化 bucket 和获取 public_endpoint
    bucket, public_endpoint = init_oss_bucket()
except Exception as e:
    print(f"OSS 初始化失败: {str(e)}")
    raise e  # 不再使用备用配置，因为 bucket 必须在武汉区域

# 设置全局请求超时
oss2.defaults.connection_pool_timeout = 30
oss2.defaults.connect_timeout = 30
oss2.defaults.read_timeout = 60

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
            image_urls = []
            
            for idx, result in enumerate(rsp.output.results):
                # 获取图片数据
                img_response = requests.get(result.url)
                if img_response.status_code != 200:
                    continue
                
                # 生成文件名
                file_name = f"{data['eventType']}_{data['eventName']}_{idx}.png"
                # OSS对象名
                oss_object_name = f"{oss_folder}/{file_name}"
                
                try:
                    # 修改上传逻辑
                    retry_times = 3
                    for attempt in range(retry_times):
                        try:
                            upload_result = bucket.put_object(oss_object_name, img_response.content)
                            if upload_result.status == 200:
                                # 构建公网访问URL
                                public_url = f"https://{public_endpoint}/{oss_object_name}"
                                image_urls.append(public_url)
                                print(f"图片上传成功：{public_url}")
                                break
                        except Exception as e:
                            if attempt == retry_times - 1:  # 最后一次重试
                                print(f"上传到OSS失败（第{attempt + 1}次尝试）：{str(e)}")
                                continue
                            print(f"上传失败，正在重试（第{attempt + 1}次）：{str(e)}")
                            time.sleep(1)  # 等待1秒后重试

                except Exception as e:
                    print(f"上传到OSS失败：{str(e)}")
                    continue

            if image_urls:
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
                    'message': '所有图片上传失败',
                    'data': None
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