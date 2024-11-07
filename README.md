# 湘韵传承——湖湘文化国际传播效果分析系统
该系统专注于分析湖湘文化在全球范围内的传播效果，以增强其国际影响力。产品定位为一款面向文化研究者，文化爱好者，文化传播者的专业分析工具。系统通过大数据和人工智能技术，帮助用户全面评估湖湘文化在国际传播中的表现，同时制定有效的传播策略以及宣传作品。

数据库设计：
    收集湖南省各市的景点以及各景点下不同平台海内外游客在社交平台的评论 -> [./doc/database.xlsx](./doc/database.xlsx)

通过调用ai大模型经过微调后对情感分析结果进行详细解释并可视化展示  

### 1.产品设计
#### 1.1 产品使命、口号和策略
##### 1.1.1 使命
加强湖湘文化的国际传播能力建设，让世界走进湖湘。
##### 1.1.2 使命口号
“湘韵传承，触手可及”。
##### 1.1.3 目标用户
* 文化研究者：关注文化传播的效果，帮助其在文化传播领域的研究提供数据支撑。
* 文化爱好者：关注文化本身，帮助其领略湖湘文化的魅力。
* 文化传播者：推动湖湘文化的跨国传播，增加全球受众的参与度。
##### 1.1.4 如何获得用户
* 学术合作：通过与国内外高校和文化研究机构合作，提供便利的文化传播数据获取。
* 社媒推广：通过短视频和社交媒体展示用户与湖湘文化的互动体验，吸引兴趣相投的受众参与。
* 地域定制广告精准投放：根据系统生成的地域受众画像，针对不同区域的投放个性化广告推广内容
##### 1.1.5 团队优势
* 多平台数据采集与处理能力
* 精细的全球情感反馈分析
* 时空传播路径与情感演化可视化
* 关键节点识别与精准用户画像
* 智能视频生成与精准广告投放
##### 1.1.6 如何做到差异化
* 湖湘文化特定领域聚焦
* 全球用户情感细腻度分析
* 时空传播路径与情感演化趋势展示
* 关键节点识别与受众画像构建
* 历史人物和传统美食的虚拟对话体验
* 自动化内容生成与个性化广告投放
#### 1.2 产品定义
湖湘文化国际传播效果分析系统是一款基于大数据分析、自然语言处理与情感计算的综合性平台，旨在为湖湘文化在全球范围内的传播效果提供全面、精准的评估和量化分析。系统聚焦红色文化、饮食文化、民俗文化、名胜古迹及非遗技艺五大主题，利用多源数据采集、时空动态追踪、情感细腻度分析等技术，从多维度动态监测文化传播路径、情感演化与受众反馈，精准识别关键传播节点及情感反应模式。系统通过数据可视化和传播策略生成，为学者和文化传播者提供科学的传播优化建议，助力湖湘文化走向国际，提升其全球影响力和接受度。
##### 1.2.1 解决的问题
* 对湖湘文化的分析缺少数据支撑
* 缺乏有效的湖湘文化传播渠道
* 年轻一代对湖湘文化了解不足
* 国际用户对湖湘文化缺乏认识
* 文化遗产和非遗技艺传承困难
##### 1.2.2 对客户的价值（采用用户故事描述，包含用户、活动和价值三个要素）
作为（用户），完成了（活动），带来什么（价值）
举例：作为一个“网站管理员”，我想要“统计每天有多少人访问了我的网站”，以便于“我的赞助商了解我的网站会给他们带来什么收益。”需要注意的是用户故事不能够使用技术语言来描述，要使用用户可以理解的业务语言来描述。参考链接   http://www.scrumcn.com/agile/scrum/4823.html
##### 1.2.3 解决方案：网站、微信小程序或者Android应用

### 2.产品设计
参考【实战技能】产品设计小文集锦  https://mp.weixin.qq.com/s/g_3_mPP5U1qjMal4BU6Q3w

### 3.产品实现
#### 3.1 用户体验设计考虑的因素
#### 3.2 产品所用编程语言及IDE、平台、框架等，写明版本号，可用表格表示，并写在项目的readme.md中
|条目名称|条目内容|版本号|备注|
|:--|--|---|--:|
|程序设计语言|Python|3.12||
|程序设计语言|Vue|5.0.8||
|IDE|Visual Studio Code|1.95.1||
|框架|Django|5.1.3||
|原型设计工具|Axure RP|11||
#### 3.3 代码仓库链接及代码提交历史截图 
包括每个人提交的次数截图
注意：理解git和github代码仓库原理
#### 3.4 安装、设计、开发中遇到的主要问题及解决方法汇总，可用表格表示，并用md或者wiki存储在项目仓库中

|问题类别|问题名称|发生原因|解决办法|
|:--|--|---|--:|
|||||
#### 3.5 软件概要设计
https://github.com/bettermorn/ACMWDevHubPPT/blob/master/UploadImg/%E8%AE%BE%E8%AE%A1%E6%96%87%E6%A1%A3%E7%9B%B8%E5%85%B3%E5%9B%BE%E7%89%87.png
![设计文档图片](https://github.com/bettermorn/ACMWDevHubPPT/blob/master/UploadImg/%E8%AE%BE%E8%AE%A1%E6%96%87%E6%A1%A3%E7%9B%B8%E5%85%B3%E5%9B%BE%E7%89%87.png)
#####  3.5.1 系统架构图，如Web应用的三层架构
注意：通常架构图从底向上绘制较普遍，从左到右较少，可根据实际情况选择
#####  3.5.2 基础设施图，如只有一台服务器，可不画。
#####  3.5.3 如果使用数据分析或者大数据/人工智能算法模型设计方法/区块链技术/数字孪生（虚拟现实XR）应用，请说明。
* 选择算法模型的原因
* 比较多种算法模型的实际效果，包括理论和指标
#####  3.5.4 数据库设计：包括E-R图即可，可使用数据库工具基于已有的数据库表逆向生成
#####  3.5.5 接口设计：重要的业务功能（可与用户故事对应）和工具类设计
|接口名称|接口功能|输入变量或对象|输出对象|备注|
|:--|--|---|---|--:|
|payAli|调用Alipay接口|inputObj1，inputObj2，。。。|outputobj1，outputobj2，。。。|需向支付宝申请付款账号|

列出方法描述，包括方法名，输入变量（如果有），返回值（如果有），可参考
微信支付API统一下单 https://pay.weixin.qq.com/wiki/doc/api/app/app.php?chapter=9_1
* 工具 Swagger https://swagger.io/
* Java服务器端设计，例如Spring MVC，可使用JavaDoc自动生成，也可使用[APIFox](https://apifox.com/)自动生成
#####  3.5.6 前端设计，例如 使用[jQuery](https://jquery.com/)、[BootStrap](https://getbootstrap.com/)或者[React](https://react.dev/)、Vue.js框架等  
#### 3.6 软件质量
##### 3.6.1 质量控制和保证方法
* 代码需要增加必要的日志
* 代码需要增加异常和错误处理
##### 3.6.2 质量工具使用
* 展示遵循Java代码规范的p3c扫描记录。 https://github.com/alibaba/p3c 在IDE中可安装插件Alibaba Java Coding Guidelines，扫描记录中不能有blocker。
* 展示遵循Python 代码规范PEP8的结果。 对代码 Pycharm IDE，参考https://www.jetbrains.com/help/pycharm/tutorial-code-quality-assistance-tips-and-tricks.html 。对VSCode IDE，使用[autopep8](https://marketplace.visualstudio.com/items?itemName=ms-python.autopep8)  automatically formats Python code to conform to the PEP8 style guide. autopep8插件可自动格式化 Python 代码，使其符合 PEP8 风格. 
参考
> * How To Encourage Best Practices in Python Programming By Complying With PEP8 Style Guide  https://henryeleonu.com/how-to-encourage-best-practices-in-python-programming-by-complying-with-pep8-style-guide
> * Python Code Quality: Tools & Best Practices https://realpython.com/python-code-quality/
* 展示Pylint的Python代码语义分析结果。 参考https://code.visualstudio.com/docs/python/linting, [Pylint For VS Code](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint), [Pylint Plugin for IntelliJ IDEA & PyCharm](https://plugins.jetbrains.com/plugin/11084-pylint), 注意：语义分析能突出显示Python 源代码中的语义和风格问题，通常能帮助识别并纠正可能导致错误的细微编程错误或编码实践。例如，语义检查可以检测到未定义变量的使用、未定义函数的调用、缺失的括号，甚至更细微的问题，如试图重新定义内置类型或函数。语法检查有别于格式化，因为语法检查分析的是代码的运行方式并检测错误，而格式化只是重构代码的外观。
* Java代码复杂度，展示插件metricsreloaded的运行结果，也可安装插件CodeMetrics查看复杂度
#### 3.7 代码统计
* Jetbrain系列IDE可以使用Statistic插件
* VS Code可用VS Code Counter插件
##### 模块数
例如代码的文件目录、包等。
##### 行数
可以分不同程序语言说明。通常插件会完成此功能。
