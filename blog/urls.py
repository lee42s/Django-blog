"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from .views import admin_home,HomeView,UserRegisterView,home,UserPasswordChangeView,UserPasswordDoneView
from blog import views
from blog import settings
urlpatterns = [
    #회원,관리자로그인 시 35줄 실행 ,비회원 로그인시 에러메세지
    url(r'^$', home, name='home'),
    #관리자
    url(r'^admin/', admin.site.urls),
    url(r'^manager/',admin_home, name='manager_home'),
    url(r'^member/', include('member.urls', namespace='member')),
    #사용자
    url(r'^blog$', HomeView.as_view(), name='blog_home'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'},name='logout'),
    url(r'^blog/accounts/login/$', auth_views.login, {'template_name': 'registration/login.html'},name='login'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^accounts/register/$', UserRegisterView.as_view(), name='register'),
    url(r'^accounts/password_change/$', UserPasswordChangeView.as_view(), name='password_change'),
    url(r'^accounts/password_change_done/$', UserPasswordDoneView.as_view(),name='password_change_done'),
    url(r'^ajax/validate_username/$', views.validate_username, name="validate_username"),

]