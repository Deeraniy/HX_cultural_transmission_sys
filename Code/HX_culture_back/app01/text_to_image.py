import os
from dashscope import ImageSynthesis
import dashscope
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
from http import HTTPStatus
import oss2
from IPython.display import Image as IPyImage, display

access_key_id = os.getenv("ALIYUN_ACCESS_KEY_ID")
access_key_secret = os.getenv("ALIYUN_ACCESS_KEY_SECRET")
endpoint = 'https://oss-cn-wuhan-lr.aliyuncs.com'
bucket_name = 'hx-cultural-images'
oss_folder = 'text_to_graph'

dashscope.api_key = API_KEY

# 初始化 OSS bucket
auth = oss2.Auth(access_key_id, access_key_secret)
bucket = oss2.Bucket(auth, endpoint, bucket_name)

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

# 可选：也将文件保存到本地目录
local_save_dir = '/mnt/oss/text_to_graph/'
os.makedirs(local_save_dir, exist_ok=True)

if rsp.status_code == HTTPStatus.OK:
    for result in rsp.output.results:
        file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
        img_data = requests.get(result.url).content

        # ✅ 上传到 OSS
        oss_object_name = f"{oss_folder}/{file_name}"
        upload_result = bucket.put_object(oss_object_name, img_data)

        if upload_result.status == 200:
            public_url = f"https://{bucket_name}.oss-cn-wuhan-lr.aliyuncs.com/{oss_object_name}"
            print(f"✅ 上传成功！公网访问地址：{public_url}")

            # ✅ 可选：同时保存到本地（如果你服务器上需要保留备份）
            save_path = os.path.join(local_save_dir, file_name)
            with open(save_path, 'wb') as f:
                f.write(img_data)
            print(f"本地已保存：{save_path}")

            # ✅ 展示图片（用公网 URL）
            display(IPyImage(url=public_url))
        else:
            print(f"❌ 上传失败，状态码: {upload_result.status}")
else:
    print('❌ 图像生成失败')
    print(f"status_code: {rsp.status_code}, code: {rsp.code}, message: {rsp.message}")