from django.urls import re_path
from django.contrib.auth.views import LoginView

from . import views

app_name = 'users'

urlpatterns = [
    # Login Page
    re_path(r'^login/$', LoginView.as_view(template_name='users/login.html'), name = 'login'), 
    # Logout Page
    re_path(r'^logout/$', views.logout_view, name='logout'),
    # Register Page
    re_path(r'^register/$', views.register, name='register'),
]
