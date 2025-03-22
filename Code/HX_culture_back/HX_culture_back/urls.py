from django.urls import path
from django.urls import re_path as url
from app01 import spot_sentiments_analyze, view, city, food, folk, publicity
from app01 import spot,collaborative_filter,casual_impact
from . import testdb,search,search2
from django.conf import settings
from django.conf.urls.static import static
from app01 import tags,views,food,search,city,cloud,comment,spot,view,lda_topic_extractor,preview,comment_tokenizer,liter_comment_tokenizer,literature,liter_sentiments_analyze,food_sentiments_analyze,food_comment_tokenizer,folk_comment_tokenizer,folk_sentiments_analyze,user,tag_details
<<<<<<< Updated upstream
from app01 import text_to_image

=======
from app01.filter_for_comments.filter import get_filtered_comments_by_tag
>>>>>>> Stashed changes
urlpatterns = [

    url(r'^testdb/$', testdb.testdb),
    # 上传头像
#     path('upload/avatar', views.UploadAvatar.as_view(), name='upload_avatar'),
#     url(r'^search-form/$', search.search_form),
#     url(r'^search/$', search.search),
#     url(r'^search-post/$', search2.search_post),
    url(r'^classes/',view.classes),
    url(r'^register/',user.register_user),
    url(r'^login/',user.verify_user),
    url(r'^get_city/',city.get_city_list),
    url(r'^get_average_score_by_bi_month/',comment.get_average_score_by_bi_month),
    url(r'^get_comment_list_recent/',comment.get_comment_list_recent),
    url(r'^get_comment_time_span/',comment.get_comment_time_span),
    url(r'^get_comment_count_last_12_months/',comment.get_comment_count_last_12_months),
    url(r'^get_comment_ip_count/',comment.get_comment_ip_count),
    url(r'^get_spot/',spot.get_spot_list),
    url(r'^preview/',preview.preview),

    url(r'^get_spot_by_name/',spot.get_spot_by_name),
    url(r'^get_comment/',comment.get_comment_list_spot),
    url(r'^get_literature_by_type/',literature.get_literature_by_type),

    url(r'^spot_sentiments_analyze/',spot_sentiments_analyze.sentiments_analyze),
    url(r'^liter_sentiments_analyze/',liter_sentiments_analyze.sentiments_analyze),
    url(r'^food_sentiments_analyze/',food_sentiments_analyze.sentiments_analyze),
    url(r'^folk_sentiments_analyze/',folk_sentiments_analyze.sentiments_analyze),
    url(r'^spot_sentiments_result/',spot_sentiments_analyze.sentiments_result),
    url(r'^liter_sentiments_result/',liter_sentiments_analyze.sentiments_result),
    url(r'^food_sentiments_result/',food_sentiments_analyze.sentiments_result),
    url(r'^folk_sentiments_result/',folk_sentiments_analyze.sentiments_result),
    url(r'^spot_generate_report/',spot_sentiments_analyze.generate_report),
    url(r'^liter_generate_report/',liter_sentiments_analyze.generate_report),
    url(r'^food_generate_report/',food_sentiments_analyze.generate_report),
    url(r'^folk_generate_report/',folk_sentiments_analyze.generate_report),
    url(r'^spot_sentiments_count/',spot_sentiments_analyze.sentiments_result_total_count),
    url(r'^liter_sentiments_count/',liter_sentiments_analyze.sentiments_result_total_count),
    url(r'^food_sentiments_count/',food_sentiments_analyze.sentiments_result_total_count),
    url(r'^folk_sentiments_count/',folk_sentiments_analyze.sentiments_result_total_count),
    url(r'^spot_get_word_frequency/',comment_tokenizer.get_word_frequency),
    url(r'^liter_get_word_frequency/',liter_comment_tokenizer.get_word_frequency),
    url(r'^food_get_word_frequency/',food_comment_tokenizer.get_word_frequency),
    url(r'^folk_get_word_frequency/',folk_comment_tokenizer.get_word_frequency),
    url(r'^spot_lda_analyze/',lda_topic_extractor.lda_analyze),
    url(r'^liter_lda_analyze/',lda_topic_extractor.lda_analyze_literature),
    url(r'^food_lda_analyze/',lda_topic_extractor.lda_analyze_food),
    url(r'^folk_lda_analyze/',lda_topic_extractor.lda_analyze_folk),
    url(r'^spot_get_comment_list/',comment.get_comment_list_spot),
    url(r'^liter_get_comment_list/',comment.get_comment_list_literature),
    url(r'^food_get_comment_list/',comment.get_comment_list_food),
    url(r'^folk_get_comment_list/',comment.get_comment_list_folk),
    url(r'^spot_get_cloud/',cloud.get_cloud),
    url(r'^liter_get_cloud/',cloud.get_cloud_literature),
    url(r'^food_get_cloud/',cloud.get_cloud_food),
    url(r'^get_food/',food.get_food_list),# get_food_list获取美食全部详细信息，把名称和图片展示asider.sider.bar
    url(r'^get_food_influence/',food.get_food_influence),# get_food_list获取美食全部详细信息，把名称和图片展示asider.sider.bar
    url(r'^get_folkcustom/',folk.get_folkcustom_list),# get_folkcustom_list获取 folkcustom全部详细信息，把名称和图片等展示
    url(r'^get_folk_influence/',folk.get_folk_influence),
    url(r'^get_all_node/',search.get_all_node),
        # 上传头像
    url(r'^get_user_preference/$', collaborative_filter.get_user_preference),
    url(r'^get_all_tags/', tags.get_all_tags),
    url(r'^get_tag_details/', tag_details.get_tag_details),
    url(r'^user$', user.get_user_info, name='get_user_info'),  # GET 请求获取用户信息
    url(r'^user/update$', user.update_user_info, name='update_user'),  # PUT 请求处理更新用户信息
    url(r'^user/upload$', user.upload_avatar, name='upload_avatar'),  # 添加头像上传路由
    url(r'^api/tag/view$', tags.view_tag),
    url(r'^api/tag/like$', tags.toggle_like),
    url(r'^api/tag/favorite$', tags.toggle_favorite),
    url(r'^api/tag/status$', tags.get_tag_status),
    url(r'^get_user_tag_status$', tags.get_user_tag_status),
    url(r'^api/tag/by_origin$', tags.get_tag_by_theme_and_origin),
    url(r'^api/tag/by_origins$', tags.get_tags_by_theme_and_origins),
    url(r'^get_casual_impact/', casual_impact.sentiments_time_series),
    url(r'^generate_publicity/', publicity.generate_publicity_report),
<<<<<<< Updated upstream
    path('api/report/generate_image/', text_to_image.generate_publicity_image),
=======
    url(r'^get_filtered_comments_by_tag/', get_filtered_comments_by_tag),
>>>>>>> Stashed changes
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


