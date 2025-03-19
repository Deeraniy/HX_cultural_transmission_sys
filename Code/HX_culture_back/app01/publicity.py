from zhipuai import ZhipuAI
import os
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

API_KEY = os.getenv("1af4f35363ea97ed269ee3099c04f7f3.3AGroi22UtegCtjf", "1af4f35363ea97ed269ee3099c04f7f3.3AGroi22UtegCtjf")
client = ZhipuAI(api_key=API_KEY)

# 定义不同平台的提示模板
PLATFORM_PROMPTS = {
    # 一、社交种草平台
    "小红书": lambda title, tags, content: f"""请生成一篇小红书风格的文案：
🎯 标题：{title}
🏷️ 相关标签：{tags}
📝 原始内容：{content}
✍️ 要求：
1. 标题吸引眼球，突出重点
2. 分点描述，每点都要有emoji
3. 语言亲切自然，富有感染力
4. 最后加上3-5个相关话题标签""",

    "微博": lambda title, tags, content: f"""作为资深湖湘文化传播策划师，请优化以下内容以适应微博传播：
📌 标题：{title}（要求：热搜式标题+话题引导）
🏷️ 标签：主话题#{tags}#，配合3-5个相关话题
📱 形式：图文结合，配图文案点题
📢 调性：简短有力，突出传播性，设置互动机制
📝 原始内容：{content}
✍️ 优化要求：控制在140字内，设计2-3个互动话题，增加转发激励""",

    # 二、短视频平台
    "抖音": lambda title, tags, content: f"""请生成一个抖音视频文案：
🎯 标题：{title}
🏷️ 相关标签：{tags}
📝 原始内容：{content}
✍️ 要求：
1. 开场吸引眼球
2. 节奏紧凑，语言简洁
3. 突出视觉和动感元素
4. 设计2-3个互动引导""",

    "B站": lambda title, tags, content: f"""请生成一个B站视频介绍：
🎯 标题：{title}
🏷️ 相关标签：{tags}
📝 原始内容：{content}
✍️ 要求：
1. 标题有梗，吸引二次元用户
2. 内容专业但不失趣味
3. 加入适当的网络用语
4. 设计弹幕互动点""",

    # 三、政务发布平台
    "政府平台": lambda title, tags, content: f"""请生成一篇政务平台发布内容：
🎯 标题：{title}
🏷️ 相关标签：{tags}
📝 原始内容：{content}
✍️ 要求：
1. 语言规范严谨
2. 突出政策导向
3. 强调社会效益
4. 注重数据支撑""",

    "党建平台": lambda title, tags, content: f"""请生成一篇党建平台内容：
🎯 标题：{title}
🏷️ 相关标签：{tags}
📝 原始内容：{content}
✍️ 要求：
1. 突出思想引领
2. 体现理论深度
3. 联系实际工作
4. 总结经验启示""",

    # 四、新闻媒体报道
    "新闻媒体": lambda title, tags, content: f"""请生成一篇新闻报道：
🎯 标题：{title}
🏷️ 相关标签：{tags}
📝 原始内容：{content}
✍️ 要求：
1. 标题新闻性强
2. 遵循5W1H原则
3. 客观报道事实
4. 突出新闻价值""",

    # 五、补充模板类型
    "海外传播": lambda title, tags, content: f"""请生成一篇面向海外的文化传播内容：
🌏 标题：{title}
🏷️ 相关标签：{tags}
📝 原始内容：{content}
✍️ 要求：
1. 注重文化解读
2. 突出国际视角
3. 避免文化误解
4. 增进文化共鸣""",

    "线下物料": lambda title, tags, content: f"""请设计线下宣传物料文案：
📑 标题：{title}
🏷️ 相关标签：{tags}
📝 原始内容：{content}
✍️ 要求：
1. 突出视觉效果
2. 文字简洁有力
3. 便于快速阅读
4. 突出活动亮点""",

    "研学活动": lambda title, tags, content: f"""请设计研学活动方案：
🎒 对象：青少年群体
📚 模块：知识传授+实践体验+互动探究
🎯 目标：寓教于乐，传承文化
📝 原始内容：{content}
✍️ 要求：设计3个课程模块，配套1个实践活动""",

    "商业合作": lambda title, tags, content: f"""请生成商业合作推广方案：
💼 形式：品牌联名/授权合作
📈 亮点：文化IP价值转化
🎯 目标：商业价值与文化传播双赢
📝 原始内容：{content}
✍️ 要求：明确商业权益，设定营销指标""",

    "学术研究": lambda title, tags, content: f"""请生成学术研究报告：
🎓 类型：文化传播研究/保护研究
📚 框架：理论依据+研究方法+数据分析
🔍 重点：文化价值研究与传播效果评估
📝 原始内容：{content}
✍️ 要求：学术规范，需有理论支撑和数据论证"""
}

# 判断内容是草稿还是需求描述
def detect_content_type(content: str) -> str:
    if len(content.strip()) < 50 or any(keyword in content for keyword in ["目标", "受众", "对象", "渠道", "限制", "人群"]):
        return "需求说明"
    elif "。" in content or "，" in content:
        return "草稿文"
    else:
        return "不确定"

def generate_simple_report(data):
    """生成宣传文案的主函数"""
    try:
        # 获取基本信息
        tags = ", ".join(data.get("tags", []))
        title = data["title"]
        content = data["content"]
        platform = data["platform"]  # 新增：指定平台
        
        # 根据平台选择对应的提示模板
        if platform in PLATFORM_PROMPTS:
            prompt = PLATFORM_PROMPTS[platform](title, tags, content)
        else:
            raise ValueError(f"不支持的平台类型：{platform}")

        # 调用 LLM
        response = client.chat.completions.create(
            model="glm-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"生成失败：{str(e)}"

@require_http_methods(["POST"])
def generate_publicity_report(request):
    """处理生成宣传报告的请求"""
    try:
        data = json.loads(request.body)
        
        # 验证必要字段
        required_fields = ["title", "content", "platform", "tags"]
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'code': 400,
                    'message': f'缺少必要字段：{field}',
                    'data': None
                })
        
        # 验证平台类型
        if data["platform"] not in PLATFORM_PROMPTS:
            return JsonResponse({
                'code': 400,
                'message': f'不支持的平台类型：{data["platform"]}',
                'data': None
            })
        
        # 生成报告
        report = generate_simple_report(data)
        
        return JsonResponse({
            'code': 200,
            'message': 'success',
            'data': {
                'report': report,
                'platform': data["platform"]
            }
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
            'message': f'生成报告失败：{str(e)}',
            'data': None
        })

# 测试数据
test_data = {
    "tags": ["湖湘文化", "非遗传承"],
    "title": "千年瑶族传统，藏在湘西深处的文化瑰宝",
    "content": "瑶族传统文化展示活动将在湘西举行，展示瑶族传统服饰制作、歌舞表演等非物质文化遗产。",
    "platform": "小红书"  # 指定平台
}

if __name__ == "__main__":
    result = generate_simple_report(test_data)
    print("\n📣 生成的宣传文案如下：\n")
    print(result)