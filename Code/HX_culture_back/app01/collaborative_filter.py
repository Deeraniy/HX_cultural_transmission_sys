from django.http import JsonResponse
from django.db import connection
import numpy as np
from math import sqrt
from typing import Dict, List, Tuple

def get_user_interactions(user_id: int) -> Dict:
    """获取用户所有交互数据"""
    try:
        cursor = connection.cursor()
        
        # 1. 获取用户的标签交互数据
        cursor.execute("""
            SELECT tu.tag_id, tu.click_count, tu.is_favorite,
                   t.theme_name, t.total_clicks, t.total_likes
            FROM tag_user tu
            JOIN tag t ON tu.tag_id = t.tag_id
            WHERE tu.user_id = %s
        """, [user_id])
        direct_interactions = cursor.fetchall()
        print("标签交互数据:", direct_interactions)
        
        tag_interactions = {}
        for interaction in direct_interactions:
            tag_id = interaction[0]
            tag_interactions[tag_id] = {
                'click_count': interaction[1],
                'is_favorite': interaction[2],
                'theme_name': interaction[3],
                'total_interactions': 0,
                'sentiment_score': 0,
                'comment_count': 0
            }

        # 2. 获取用户的评论数据（从 user_comment 表）
        cursor.execute("""
            SELECT tag_id, comment_text, sentiment,
                   sentiment_confidence, like_count
            FROM user_comment
            WHERE user_id = %s
        """, [user_id])
        user_comments = cursor.fetchall()
        print("用户评论数据:", user_comments)
        
        # 处理评论数据
        for comment in user_comments:
            tag_id = comment[0]
            if tag_id not in tag_interactions:
                # 如果这个标签还没有交互记录，创建一个新的
                cursor.execute("""
                    SELECT theme_name
                    FROM tag
                    WHERE tag_id = %s
                """, [tag_id])
                theme_result = cursor.fetchone()
                theme_name = theme_result[0] if theme_result else None
                
                tag_interactions[tag_id] = {
                    'click_count': 0,
                    'is_favorite': False,
                    'theme_name': theme_name,
                    'total_interactions': 0,
                    'sentiment_score': 0,
                    'comment_count': 0
                }
            
            # 更新标签的评论相关数据
            tag_data = tag_interactions[tag_id]
            tag_data['comment_count'] += 1
            tag_data['total_interactions'] += comment[4] or 0  # like_count
            
            # 计算情感得分
            sentiment_value = 1 if comment[2] == 'positive' else \
                            -1 if comment[2] == 'negative' else 0
            confidence = float(comment[3] or 0)  # sentiment_confidence
            tag_data['sentiment_score'] += sentiment_value * confidence
        
        # 3. 获取用户点赞的评论数据
        cursor.execute("""
            SELECT uc.tag_id
            FROM comment_like cl
            JOIN user_comment uc ON cl.comment_id = uc.comment_id
            WHERE cl.user_id = %s
        """, [user_id])
        liked_comments = cursor.fetchall()
        print("用户点赞的评论:", liked_comments)
        
        # 处理点赞数据
        for liked_comment in liked_comments:
            tag_id = liked_comment[0]
            if tag_id in tag_interactions:
                tag_interactions[tag_id]['total_interactions'] += 1
        
        cursor.close()
        return calculate_final_scores(tag_interactions)
        
    except Exception as e:
        print(f"Database Error: {e}")
        return {}

def calculate_final_scores(tag_interactions: Dict) -> Dict:
    """计算最终的用户倾向得分"""
    final_scores = {}
    
    for tag_id, data in tag_interactions.items():
        # 标准化各个分数
        click_score = min(data['click_count'] / 10.0, 1.0)
        favorite_score = 1.0 if data['is_favorite'] else 0.0
        interaction_score = min(data['total_interactions'] / 20.0, 1.0)
        
        # 标准化情感得分
        sentiment_score = 0
        if data['comment_count'] > 0:
            sentiment_score = (data['sentiment_score'] / data['comment_count'] + 1) / 2
        
        # 计算综合得分
        final_scores[tag_id] = {
            'score': (
                click_score * 0.25 +
                favorite_score * 0.25 +
                interaction_score * 0.25 +
                sentiment_score * 0.25
            ),
            'theme_name': data['theme_name'],
            'components': {
                'click_score': click_score,
                'favorite_score': favorite_score,
                'interaction_score': interaction_score,
                'sentiment_score': sentiment_score
            }
        }
    
    return final_scores

def get_user_preference(request):
    """Django视图函数：获取用户倾向和推荐"""
    try:
        user_id = request.GET.get('user_id')
        if not user_id:
            return JsonResponse({
                "status": "error",
                "message": "Missing user_id parameter"
            })
            
        user_id = int(user_id)
        
        # 1. 获取用户当前的偏好
        user_preferences = get_user_interactions(user_id)
        
        # 获取主用户的所有tag_id集合
        user_tag_ids = set(user_preferences.keys())
        
        # 2. 计算用户相似度
        user_similarities = calculate_user_similarity(user_id)
        
        # 获取最相似的用户（前5个）
        similar_users = sorted(
            user_similarities.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        # 3. 获取相似用户的标签偏好（排除主用户已有的标签）
        similar_users_preferences = {}
        for sim_user_id, similarity in similar_users:
            sim_user_prefs = get_user_interactions(sim_user_id)
            # 过滤掉主用户已有的标签
            filtered_prefs = {
                tag_id: data 
                for tag_id, data in sim_user_prefs.items() 
                if tag_id not in user_tag_ids
            }
            if filtered_prefs:  # 只保存有独特偏好的相似用户
                similar_users_preferences[sim_user_id] = {
                    'similarity': similarity,
                    'preferences': filtered_prefs
                }
        
        # 4. 整理返回结果
        theme_preferences = {}
        for tag_id, data in user_preferences.items():
            theme = data['theme_name']
            if theme not in theme_preferences:
                theme_preferences[theme] = []
            theme_preferences[theme].append({
                'tag_id': tag_id,
                'score': data['score'],
                'score_components': data['components']
            })
        
        # 计算每个主题的总体倾向
        theme_scores = {}
        for theme, items in theme_preferences.items():
            if items:
                theme_scores[theme] = sum(item['score'] for item in items) / len(items)
        
        # 只返回有独特偏好的相似用户
        filtered_similar_users = [
            {
                "user_id": uid,
                "similarity_score": score,
                "preferences": similar_users_preferences[uid]['preferences']
            }
            for uid, score in similar_users
            if uid in similar_users_preferences
        ]
        
        return JsonResponse({
            "status": "ok",
            "data": {
                "theme_preferences": theme_scores,
                "detailed_preferences": theme_preferences,
                "similar_users": filtered_similar_users
            }
        })
        
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        })

def calculate_user_similarity(user_id: int) -> Dict[int, float]:
    """计算用户相似度"""
    try:
        cursor = connection.cursor()
        
        # 1. 获取所有用户的标签交互数据（移除时间限制）
        cursor.execute("""
            SELECT 
                tu1.user_id,
                COUNT(DISTINCT tu1.tag_id) as common_tags,
                COUNT(DISTINCT t1.theme_name) as common_themes,
                AVG(tu1.click_count * 0.6 + 
                    CASE WHEN tu1.is_favorite THEN 0.4 ELSE 0 END) as avg_interaction
            FROM tag_user tu1
            JOIN tag t1 ON tu1.tag_id = t1.tag_id
            JOIN tag_user tu2 ON t1.theme_name = (
                SELECT t2.theme_name 
                FROM tag_user tu3 
                JOIN tag t2 ON tu3.tag_id = t2.tag_id 
                WHERE tu3.user_id = %s AND tu3.tag_id = tu1.tag_id
            )
            WHERE tu1.user_id != %s
            GROUP BY tu1.user_id
            HAVING COUNT(DISTINCT tu1.tag_id) >= 2
        """, [user_id, user_id])
        
        potential_users = cursor.fetchall()
        
        # 2. 计算相似度分数
        similarities = {}
        for user_data in potential_users:
            other_user_id = user_data[0]
            common_tags = user_data[1]
            common_themes = user_data[2]
            avg_interaction = user_data[3] or 0  # 防止 NULL 值
            
            # 简化的相似度计算
            similarity_score = (
                min(common_tags / 5, 1) * 0.5 +  # 共同标签数量（最高权重）
                min(common_themes / 3, 1) * 0.3 + # 共同主题数量
                min(float(avg_interaction), 1) * 0.2  # 平均交互强度
            )
            
            similarities[other_user_id] = similarity_score
        
        return similarities
        
    except Exception as e:
        print(f"Error calculating user similarity: {e}")
        return {}

def predict_user_interests(user_id: int, similarities: Dict[int, float]) -> Dict[int, float]:
    """预测用户对未交互标签的兴趣度"""
    try:
        cursor = connection.cursor()
        
        # 获取相似用户的交互数据
        similar_users = sorted(
            similarities.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]  # 取前5个最相似的用户
        
        # 获取目标用户已交互的标签
        cursor.execute("""
            SELECT tag_id FROM tag_user WHERE user_id = %s
        """, [user_id])
        user_tags = set(row[0] for row in cursor.fetchall())
        
        # 预测兴趣度
        predictions = {}
        for sim_user_id, similarity in similar_users:
            cursor.execute("""
                SELECT tag_id, 
                       (click_count * 0.4 + 
                        CASE WHEN is_favorite THEN 0.6 ELSE 0 END) as score
                FROM tag_user
                WHERE user_id = %s
            """, [sim_user_id])
            
            for tag_id, score in cursor.fetchall():
                if tag_id not in user_tags:  # 只预测未交互的标签
                    if tag_id not in predictions:
                        predictions[tag_id] = {'total_sim': 0, 'weighted_score': 0}
                    predictions[tag_id]['total_sim'] += abs(similarity)
                    predictions[tag_id]['weighted_score'] += similarity * score
        
        # 计算最终预测分数
        final_predictions = {}
        for tag_id, data in predictions.items():
            if data['total_sim'] > 0:
                final_predictions[tag_id] = data['weighted_score'] / data['total_sim']
        
        return final_predictions
        
    except Exception as e:
        print(f"Error predicting interests: {e}")
        return {}