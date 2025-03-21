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
    "小红书": lambda event_info: f"""
{event_info}

请生成一篇小红书风格的文案，要求：
1. 标题必须完整包含活动名称中的关键词，并自然融入网络热词
2. 正文中至少3次自然提及活动名称中的关键词
3. 内容分点描述，每个要点配上合适的emoji
4. 设计2-3个与活动名称相关的打卡点
5. 最后的话题标签必须包含活动名称的核心词
6. 标题要吸引年轻人眼球，可以适当加入网络热词
7. 突出活动的体验感和参与感
8. 最后加上3-5个相关话题标签
9. 语言风格要活泼自然，富有感染力""",

    "微博": lambda title, tags: f"""作为资深湖湘文化传播策划师，请优化以下内容以适应微博传播：
📌 标题：{title}（要求：热搜式标题+话题引导）
🏷️ 标签：主话题#{tags}#，配合3-5个相关话题
📱 形式：图文结合，配图文案点题
📢 调性：简短有力，突出传播性，设置互动机制
✍️ 优化要求：控制在140字内，设计2-3个互动话题，增加转发激励""",

    # 二、短视频平台
    "抖音": lambda event_info, content_info: f"""
{event_info}
{content_info}

请生成一个抖音视频文案，要求：
1. 开场要有吸引力，可以设置悬念或反转
2. 内容节奏要紧凑，每20秒一个重点
3. 加入2-3个适合拍摄的画面建议
4. 设计互动引导和话题标签
5. 可以推荐2-3首配乐风格
6. 突出活动的视觉亮点和参与环节""",

    "B站": lambda event_info, content_info: f"""
{event_info}
{content_info}

请生成一个B站视频脚本，要求：
1. 标题要有梗，吸引年轻文化爱好者
2. 内容既要专业又要有趣
3. 可以加入一些二次元文化元素
4. 设计3-4个弹幕互动点
5. 突出知识性和趣味性的结合
6. 可以设计一个简单的互动环节""",

    # 三、政务发布平台
    "政府平台": lambda event_info, content_info: f"""
{event_info}
{content_info}

请生成一篇政务平台发布内容，要求：
1. 标题要庄重规范
2. 内容要突出活动的政策意义和社会价值
3. 加入相关政策支持和数据支撑
4. 强调活动的示范引领作用
5. 注重文化传承和创新的结合
6. 语言要严谨规范""",

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
        title = data["title"]
        content = data["content"]
        platform = data["platform"]
        tags = ", ".join(data.get("tags", []))
        event_name = data["eventName"]
        event_type = data["eventType"]
        promotion_tendency = data["promotionTendency"]
        promotion_method = data["promotionMethod"]
        
        # 构建活动基本信息
        event_context = f"""
活动名称：{event_name}
活动属性：{event_type}
宣传倾向：{promotion_tendency}
宣传方式：{promotion_method}
相关标签：{tags}
"""

        # 根据是否提供标题和内容构建不同的分析提示
        content_context = ""
        if title and content:
            content_context = f"""
参考标题：{title}
参考内容：{content}

请基于以上参考内容进行优化和扩展。"""
        elif title:
            content_context = f"""
参考标题：{title}

请参考这个标题的风格和重点进行内容创作，记住，标题十分重要。"""
        elif content:
            content_context = f"""
参考内容：{content}

请在保持核心信息的基础上进行优化和扩展。"""

        # 生成主要内容
        main_content = ""
        if platform in PLATFORM_PROMPTS:
            # 根据平台类型调用对应的 lambda 函数
            if platform == "小红书":
                prompt = PLATFORM_PROMPTS[platform](event_context)
            elif platform == "微博":
                prompt = PLATFORM_PROMPTS[platform](title, tags)
            else:
                # 其他平台的处理...
                prompt = PLATFORM_PROMPTS[platform](title, tags)
                
            response = client.chat.completions.create(
                model="glm-4",
                messages=[{
                    "role": "user", 
                    "content": f"""作为一名专业的文化活动策划师，请根据以下信息生成一篇富有感染力的宣传内容：

{prompt}

请确保生成的内容：
1. 紧密围绕活动主题和目标，尤其是活动名称，一定要有体现
2. 突出活动特色和亮点
3. 符合目标平台的传播特点
4. 注重文化传承和创新
5. 吸引目标受众参与互动
6. 标题必须包含活动名称中的2-3个核心词
7. 正文前100字必须明确提及完整活动名称
📢 硬性要求：
1. 活动名称"{event_name}"必须完整出现在正文前两段
2. 名称中的关键词（如"{'、'.join(event_name.split())}"）需在全文出现3次以上
🎯 创作技巧：
1. 把名称拆解为记忆点（示例："瑶族传统|文化展示|湘西盛会"）
2. 在每部分内容自然植入名称要素
3. 将名称关键词与平台特色结合（如小红书打卡点命名）

注意：
1. 不要使用 \\n 作为换行，使用 markdown 格式
2. 使用 # ## ### 等标记来标识标题层级
3. 正文内容使用段落格式，不要加多余的换行
4. 宣传策略建议部分使用规范的 markdown 格式"""
                }]
            )
            main_content = response.choices[0].message.content.strip()

        # 生成宣传策略建议
        strategy_prompt = f"""
基于以下活动信息，请生成详细的宣传策略建议：

{event_context}

请从以下几个方面提供建议（使用markdown格式）：

### 宣传策略建议

#### 1. 最佳发布时间和频率
- 具体说明发布时间和频率安排

#### 2. 内容呈现形式
- 详细说明如何通过{platform}平台进行宣传
- 根据活动特点设计内容形式

#### 3. 互动策略
- 设计与活动主题强相关的互动方案
- 提供吸引目标受众的具体方法

请确保建议具体可行，便于执行。
注意：使用markdown格式，不要使用\\n换行"""

        strategy_response = client.chat.completions.create(
            model="glm-4-air",
            messages=[{"role": "user", "content": strategy_prompt}]
        )
        strategy_content = strategy_response.choices[0].message.content.strip()

        # 组合内容和策略，使用markdown格式
        final_content = f"""
{main_content}

━━━━━━━━━━ 宣传策略建议 ━━━━━━━━━━

{strategy_content}"""

        return final_content.strip()
    except Exception as e:
        print(f"生成报告时出错: {str(e)}")
        raise e

@require_http_methods(["POST"])
def generate_publicity_report(request):
    """处理生成宣传报告的请求"""
    try:
        data = json.loads(request.body)
        
        # 验证必要字段
        required_fields = ["platform", "eventName", "eventType"]  # 修改必要字段
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