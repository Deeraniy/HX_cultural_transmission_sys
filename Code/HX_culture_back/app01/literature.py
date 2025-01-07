from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
import json
import pymysql

def get_literature_list(request):
    """获取所有文学作品列表"""
    try:
        # 创建连接
        conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                             db='hx_cultural_transmission_sys', charset='utf8')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 执行SQL，并返回影响行数
        cursor.execute("SELECT * FROM literature")
        literature_list = cursor.fetchall()

        return JsonResponse({
            'status': 'success',
            'data': list(literature_list)  # 转换为列表
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    finally:
        # 关闭游标和连接
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def get_literature_by_name(request):
    """根据名称搜索文学作品"""
    try:
        liter_name = request.GET.get('liter_name')
        if not liter_name:
            return JsonResponse({
                'status': 'error',
                'message': '文学作品名称不能为空'
            }, status=400)
        
        # 创建连接
        conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                             db='hx_cultural_transmission_sys', charset='utf8')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        
        # 模糊查询
        sql_query = "SELECT * FROM literature WHERE liter_name LIKE %s"
        cursor.execute(sql_query, ('%' + liter_name + '%'))
        literature_list = cursor.fetchall()
        
        return JsonResponse({
            'status': 'success',
            'data': list(literature_list)
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    finally:
        # 关闭游标和连接
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def get_literature_by_type(request):
    """根据文学类型名称查询文学作品"""
    try:
        type_name = request.GET.get('type_name')
        print(f"收到请求参数 type_name: {type_name}")  # 调试日志
        
        if not type_name:
            return JsonResponse({
                'status': 'error',
                'message': '文学类型名称不能为空'
            }, status=400)
        
        # 创建连接
        conn = pymysql.connect(host='120.233.26.237', port=15320, user='root', passwd='kissme77',
                             db='hx_cultural_transmission_sys', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        
        # 先查询type_id
        type_sql = "SELECT type_id FROM liter_type WHERE type_name = %s"
        cursor.execute(type_sql, (type_name,))
        type_result = cursor.fetchone()
        
        print(f"类型查询结果: {type_result}")  # 调试日志
        
        if not type_result:
            return JsonResponse({
                'status': 'error',
                'message': f'未找到文学类型: {type_name}'
            }, status=404)
        
        type_id = type_result['type_id']
        
        # 根据type_id查询文学作品
        literature_sql = "SELECT * FROM literature WHERE type_id = %s"
        cursor.execute(literature_sql, (type_id,))
        literature_list = cursor.fetchall()
        
        return JsonResponse({
            'status': 'success',
            'data': list(literature_list)
        })
        
    except Exception as e:
        import traceback
        print(f"错误详情: {str(e)}")
        print(traceback.format_exc())  # 打印完整的错误堆栈
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
