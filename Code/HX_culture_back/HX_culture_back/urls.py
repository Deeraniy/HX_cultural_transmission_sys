from django.urls import path
from django.urls import re_path as url
from app01 import view,city
from app01 import spot
from . import testdb,search,search2
from django.conf import settings
from django.conf.urls.static import static
from app01 import sentiments_analyze,city,cloud,comment,spot,view,lda_topic_extractor,sentiments_analyze
urlpatterns = [
    
    url(r'^testdb/$', testdb.testdb),
    url(r'^search-form/$', search.search_form),
    url(r'^search/$', search.search),
    url(r'^search-post/$', search2.search_post),
    url(r'^classes/',view.classes),

    url(r'^get_city/',city.get_city_list),
    url(r'^get_cloud/',cloud.get_cloud),
    url(r'^get_comment_list/',comment.get_comment_list),
    url(r'^get_average_score_by_bi_month/',comment.get_average_score_by_bi_month),
    url(r'^get_comment_list_recent/',comment.get_comment_list_recent),
    url(r'^get_comment_time_span/',comment.get_comment_time_span),
    url(r'^get_comment_count_last_12_months/',comment.get_comment_count_last_12_months),
    url(r'^get_comment_ip_count/',comment.get_comment_ip_count),
    url(r'^get_spot/',spot.get_spot_list),

    url(r'^lda_analyze/',lda_topic_extractor.lda_analyze),
    url(r'^get_spot_by_name/',spot.get_spot_by_name),
    url(r'^get_comment/',comment.get_comment_list),
    url(r'^sentiments_analyze/',sentiments_analyze.sentiments_analyze),
    


    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


