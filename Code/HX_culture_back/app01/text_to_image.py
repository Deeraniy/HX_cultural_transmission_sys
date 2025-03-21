from dashscope import ImageSynthesis
import dashscope
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests

dashscope.api_key = "sk-e184c1f6d2524d00a3eb1de084684530"

# 提示词
prompt = "画一张宣传海报，结合足球，岳麓山，臭豆腐这个元素"

print('----sync call, please wait a moment----')

# 调用图像生成
rsp = ImageSynthesis.call(
    model="wanx2.1-t2i-turbo",
    prompt=prompt,
    n=1,
    size='1024*1024'
)

# 检查返回状态并下载图片
from http import HTTPStatus

if rsp.status_code == HTTPStatus.OK:
    for result in rsp.output.results:
        file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
        print(f"保存图片为: {file_name}")
        img_data = requests.get(result.url).content
        with open(file_name, 'wb') as f:
            f.write(img_data)
        # Colab 中展示图片
        from IPython.display import Image as IPyImage, display
        display(IPyImage(file_name))
else:
    print('生成失败')
    print(f"status_code: {rsp.status_code}, code: {rsp.code}, message: {rsp.message}")