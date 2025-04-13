from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import gradio as gr
import json
import threading
import time
from zhipuai import ZhipuAI
from .config import ZHIPUAI_API_KEY

# 创建智谱AI客户端
client = ZhipuAI(api_key=ZHIPUAI_API_KEY)

# 存储 Gradio 公共链接
gradio_public_url = None

# 创建 Gradio 接口
def chat_bot(message):
    try:
        # 调用智谱AI接口
        response = client.chat.completions.create(
            model="glm-4-air",  # 或使用其他可用模型
            messages=[
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            top_p=0.7,
            max_tokens=1024
        )
        
        # 从响应中提取回答内容
        if response and hasattr(response, 'choices') and response.choices:
            answer = response.choices[0].message.content
            print(f"AI回答: {answer}")
            return answer
        else:
            error_msg = "AI响应格式错误"
            print(error_msg)
            return error_msg
            
    except Exception as e:
        error_msg = f"调用智谱AI出错: {str(e)}"
        print(error_msg)
        return "抱歉，AI助手暂时无法回答，请稍后再试。"

# 创建 Gradio 应用
demo = gr.Interface(
    fn=chat_bot,
    inputs=gr.Textbox(placeholder="请输入您的问题..."),
    outputs=gr.Textbox(),
    title="智谱AI助手",
    description="我是基于智谱AI的助手，让我们开始对话吧！",
    examples=[
        ["你好，请介绍一下你自己"],
        ["什么是红色文化？"],
        ["中国有哪些著名的红色旅游景点？"]
    ]
)

# 在单独的线程中启动 Gradio
def run_gradio():
    global gradio_public_url
    server = demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        inbrowser=False
    )
    time.sleep(5)
    if hasattr(server, 'share_url'):
        gradio_public_url = server.share_url
        print(f"Gradio running on: {gradio_public_url}")

# 启动 Gradio 服务
threading.Thread(target=run_gradio, daemon=True).start()

# Gradio 视图函数
def gradio_view(request):
    global gradio_public_url
    if not gradio_public_url:
        time.sleep(2)
    url = gradio_public_url if gradio_public_url else "http://localhost:7860"
    return render(request, 'gradio.html', {'gradio_url': url})

@csrf_exempt
def chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message", "")
            history = data.get("history", [])
            
            # 使用智谱AI处理请求
            response = chat_bot(message)
            
            return JsonResponse({
                "history": [[message, response]]
            })
        except Exception as e:
            print(f"Chat error: {e}")
            return JsonResponse({
                "error": str(e)
            }, status=500)
            
    return JsonResponse({"error": "Invalid request"}, status=400)