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
    "小红书": lambda title, tags, content: f"""作为资深湖湘文化传播策划师，请优化以下内容以适应年轻化传播：
📌 标题：{title}（要求：加入网络热词+悬念设置）
🏷️ 标签：主标签#{tags}，辅标签#体验打卡+#非遗传承
📺 形式：需包含3个拍照打卡点建议+1个互动问题
📢 渠道：小红书，调性：轻松活泼+知识干货
📝 原始内容：{content}
✍️ 优化要求：每段添加1个表情符号，使用"你"的第二人称，结尾设计2个话题讨论""",

    "微博": lambda title, tags, content: f"""作为资深湖湘文化传播策划师，请优化以下内容以适应微博传播：
📌 标题：{title}（要求：热搜式标题+话题引导）
🏷️ 标签：主话题#{tags}#，配合3-5个相关话题
📱 形式：图文结合，配图文案点题
📢 调性：简短有力，突出传播性，设置互动机制
📝 原始内容：{content}
✍️ 优化要求：控制在140字内，设计2-3个互动话题，增加转发激励""",

    # 二、短视频平台
    "抖音": lambda title, tags, content: f"""请以短视频脚本形式重构宣传内容：
🎬 标题：{title}（要求：设置冲突/反转，如"99%的人不知道的...")
📌 信息点：需突出{tags}的视觉冲击力
⏱️ 结构：黄金3秒悬念+15秒核心展示+5秒行动号召
🎵 适配音乐：建议3种BGM类型（如：国风电子/传统民乐改编）
💬 互动设计：结尾需包含挑战赛话题或打卡任务
📝 原始素材：{content}
🔧 修改要求：每20字换行，关键信息重复强调，加入口语化热梗""",

    "B站": lambda title, tags, content: f"""请以B站视频脚本形式重构宣传内容：
🎬 标题：{title}（要求：科普向+干货感）
📌 分区：文化/人文历史
⏱️ 结构：开场创意+干货主体+互动引导，建议时长5-7分钟
🎨 风格：硬核科普+趣味解说，可加入动画元素
📝 原始素材：{content}
🔧 修改要求：加入专业知识点，设计弹幕互动点，结尾设置悬念""",

    # 三、政务发布平台
    "政府平台": lambda title, tags, content: f"""请将内容转化为政务信息通报格式：
🏛️ 发文单位：湖南省文化和旅游厅（需前置）
📜 政策依据：加入《文化保护与传承相关政策》条目
⭐ 核心要素：突出文化保护成果+惠民措施
📊 数据支撑：需补充参与人次/资金投入/保护成果等数据
📝 原始材料：{content}
✒️ 修改要求：使用仿宋字体分段，专业术语规范，添加2处领导讲话引用""",

    "党建平台": lambda title, tags, content: f"""请将内容转化为党建宣传格式：
🏛️ 主题：弘扬传统文化，践行社会主义核心价值观
📜 理论依据：习近平总书记关于文化建设的重要论述
⭐ 重点：突出党的领导、群众路线、文化自信
📊 成果展示：文化传承与创新的具体实践
📝 原始材料：{content}
✒️ 修改要求：突出政治性、思想性，结合时代特色""",

    # 四、新闻媒体报道
    "新闻媒体": lambda title, tags, content: f"""请按新闻通稿标准改写：
📰 标题：{title}（副标题：展现文化创新亮点）
🔍 新闻要素：5W1H原则需完整呈现
👥 采访对象：加入传承人+市民+专家三方视角
📷 配图建议：描述3个关键画面拍摄建议
📝 原始资料：{content}
✍️ 修改方向：采用倒金字塔结构，首段包含核心信息，加入2处直接引语""",

    # 五、补充模板类型
    "海外传播": lambda title, tags, content: f"""请生成适合海外社交平台的文案：
🌍 平台：Instagram/Facebook
🎨 文化符号：需说明{tags}的国际对应物
🎯 目标：突出中国文化特色，促进文化互鉴
📝 原始内容：{content}
✍️ 要求：中英双语，配色方案需符合国际审美，突出视觉冲击力""",

    "线下物料": lambda title, tags, content: f"""请生成适合线下展示的文案：
🖼️ 场景：展馆/户外广告
📐 规格：主视觉、说明文案、导览设计
🎨 视觉：传统元素现代呈现
📝 原始内容：{content}
✍️ 要求：层次分明，重点突出，适合远近距离阅读""",

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