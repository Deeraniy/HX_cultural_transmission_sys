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

# 提示词
prompt = "画一张宣传海报，结合足球，岳麓山，臭豆腐这个元素"

print('----开始生成图片，请稍等片刻----')

# 调用 DashScope 图像生成
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