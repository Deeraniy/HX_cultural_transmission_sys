from django.shortcuts import HttpResponse, JsonResponse
import pymysql

# 添加节点关系
def add_node_relation(request):
    if request.method == 'POST':
        node1 = request.POST.get('node1')
        node2 = request.POST.get('node2')
        relation = request.POST.get('relation')
        status = request.POST.get('status')

        if node1 and node2 and relation and status:
            # 创建连接
            conn = pymysql.connect(host='120.233.26.237', port=3306, user='root', passwd='song',
                                   db='hx_cultural_transmission_sys', charset='utf8')
            # 创建游标
            cursor = conn.cursor()
            try:
                # 执行SQL插入语句
                sql = "INSERT INTO node_relations (node1, node2, relation, status) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (node1, node2, relation, status))
                conn.commit()
                return HttpResponse("添加成功")
            except Exception as e:
                conn.rollback()
                return HttpResponse(f"添加失败: {e}")
            finally:
                # 关闭游标
                cursor.close()
                # 关闭连接
                conn.close()
        else:
            return JsonResponse({"error": "未提供节点1、节点2、关系或审核状态"})
    else:
        return JsonResponse({"error": "不是POST请求!"})

def delete_node_relation(request):
    if request.method == 'POST':
        node1 = request.POST.get('node1')
        node2 = request.POST.get('node2')
        relation = request.POST.get('relation')

        if node1 and node2 and relation:
            # 创建连接
            conn = pymysql.connect(host='120.233.26.237', port=3306, user='root', passwd='song',
                                   db='hx_cultural_transmission_sys', charset='utf8')
            # 创建游标
            cursor = conn.cursor()
            try:
                # 执行删除语句
                sql = "DELETE FROM node_relations WHERE node1 = %s AND node2 = %s AND relation = %s"
                cursor.execute(sql, (node1, node2, relation))
                conn.commit()
                return HttpResponse("删除成功")
            except Exception as e:
                conn.rollback()
                return HttpResponse(f"删除失败: {e}")
            finally:
                # 关闭游标
                cursor.close()
                # 关闭连接
                conn.close()
        else:
            return JsonResponse({"error": "未提供节点1、节点2或关系"})
    else:
        return JsonResponse({"error": "不是POST请求!"})

# 变更节点审核状态
def update_node_status(request):
    if request.method == 'POST':
        node1 = request.POST.get('node1')
        node2 = request.POST.get('node2')
        relation = request.POST.get('relation')
        new_status = request.POST.get('new_status')

        if node1 and node2 and relation and new_status:
            # 创建连接
            conn = pymysql.connect(host='120.233.26.237', port=3306, user='root', passwd='song',
                                   db='hx_cultural_transmission_sys', charset='utf8')
            # 创建游标
            cursor = conn.cursor()
            try:
                # 执行更新语句
                sql = "UPDATE node_relations SET status = %s WHERE node1 = %s AND node2 = %s AND relation = %s"
                cursor.execute(sql, (new_status, node1, node2, relation))
                conn.commit()
                return HttpResponse("更新成功")
            except Exception as e:
                conn.rollback()
                return HttpResponse(f"更新失败: {e}")
            finally:
                # 关闭游标
                cursor.close()
                # 关闭连接
                conn.close()
        else:
            return JsonResponse({"error": "未提供节点1、节点2、关系或新状态"})
    else:
        return JsonResponse({"error": "不是POST请求!"})
