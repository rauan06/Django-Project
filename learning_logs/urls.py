from django.urls import re_path
from . import views

app_name = 'learning_logs'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^topics/$', views.topics, name = 'topics'),
    re_path(r'^topics/(?P<topic_id>\d+)/$', views.topic, name = 'topic'),
    re_path(r'^new_topic/$', views.new_topic, name = 'new_topic'),
    re_path(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name = 'new_entry'),
    re_path(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name = 'edit_entry'),
    re_path(r'^delete_topic/(?P<topic_id>\d+)/$', views.delete_topic, name = 'delete_topic'),
]
