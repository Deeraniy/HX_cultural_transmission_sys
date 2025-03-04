from django.shortcuts import render, redirect, HttpResponse
import pymysql
from django.http import JsonResponse

def get_all_node(request):
    # 连接到数据库
    conn = pymysql.connect(host='60.215.128.117', port=15320, user='root', passwd='kissme77',
                           db='hx_cultural_transmission_sys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 知识图谱节点列表
    knowledge_graph_nodes = []
    links = []  # 存储节点之间的链接

    # 定义核心节点
    node = {
        "id": "core",
        "name": "湖湘文化",
        "type": "Core"
    }
    knowledge_graph_nodes.append(node)

    # 定义主题节点
    themes = [
        {"id": "theme1", "name": "饮食文化", "type": "Theme"},
        {"id": "theme2", "name": "名胜古迹", "type": "Theme"},
        {"id": "theme3", "name": "非遗民俗", "type": "Theme"},
        {"id": "theme4", "name": "影视文学", "type": "Theme"}
    ]

    for theme in themes:
        knowledge_graph_nodes.append(theme)
        # 生成从核心节点到主题节点的链接
        links.append({"source": "core", "target": theme["id"],"name":"连接"})

    try:
        # 查询景点数据并关联到 "名胜古迹"
        cursor.execute("SELECT * FROM scenicspot")
        spot_list = cursor.fetchall()
        for spot in spot_list:
            node = {
                "id": f"spot_{spot['spot_id']}",
                "name": spot["spot_name"],
                "categories": "Spot",
                "properties": {
                    "spot_id": spot["spot_id"],
                    "city_id": spot["city_id"],
                    "spot_name": spot["spot_name"],
                    "image_url": spot["image_url"],
                    "description_url": spot["description"],
                }
            }
            knowledge_graph_nodes.append(node)
            # 创建链接：将景点添加到 "名胜古迹" 主题下
            links.append({"source": "theme2", "target": f"spot_{spot['spot_id']}","name":"连接"})

        # 查询文学作品数据并关联到 "影视文学"
        cursor.execute("SELECT * FROM literature")
        literature_list = cursor.fetchall()
        for literature in literature_list:
            node = {
                "id": f"literature_{literature['liter_id']}",
                "name": literature["liter_name"],
                "categories": "Literature",
                "properties": {
                    "literature_id": literature["liter_id"],
                    "img_url": literature["image_url"],
                    "description_url": literature["description"],
                    "text": literature["text"]
                }
            }
            knowledge_graph_nodes.append(node)
            # 创建链接：将文学作品添加到 "影视文学" 主题下
            links.append({"source": "theme4", "target": f"literature_{literature['liter_id']}","name":"连接"})

        # 查询食物数据并关联到 "饮食文化"
        cursor.execute("SELECT * FROM food")
        food_list = cursor.fetchall()
        for Food in food_list:
            node = {
                "id": f"food_{Food['food_id']}",
                "name": Food["food_name"],
                "categories": "Food",
                "properties": {
                    "food_id": Food["food_id"],
                    "food_name": Food["food_name"],
                    "description_url": Food["description"],
                    "img_url": Food["image_url"],
                    "text": Food["text"],
                }
            }
            knowledge_graph_nodes.append(node)
            # 创建链接：将食物添加到 "饮食文化" 主题下
            links.append({"source": "theme1", "target": f"food_{Food['food_id']}","name":"连接"})

        # 查询民俗数据并关联到 "非遗民俗"
        cursor.execute("SELECT * FROM folk")
        folk_list = cursor.fetchall()
        for folk in folk_list:
            node = {
                "id": f"folk_{folk['folk_id']}",
                "name": folk["folk_name"],
                "categories": "Folk",
                "properties": {
                    "folk_id": folk["folk_id"],
                    "folk_name": folk["folk_name"],
                    "folk_type": folk["folk_type"],
                    "text": folk["description"],
                    "img_url": folk["image_url"],
                }
            }
            knowledge_graph_nodes.append(node)
            # 创建链接：将民俗添加到 "非遗民俗" 主题下
            links.append({"source": "theme3", "target": f"folk_{folk['folk_id']}","name":"连接"})

    finally:
        # 关闭游标和连接
        cursor.close()
        conn.close()

    # 返回节点和链接的 JSON 数据
    return JsonResponse({"data": knowledge_graph_nodes, "links": links})
