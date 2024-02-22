from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^topics/$', views.topics, name = "topics"),
    re_path(r'^topics/(?P<topic_id>\d+)/$', views.topic, name = "topic"),
    re_path(r'^new_topic/$', views.new_topic, name = 'new_topic')
]
