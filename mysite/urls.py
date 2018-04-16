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
from .views import admin_home,UserRegisterView,home,UserPasswordChangeView,UserPasswordDoneView
from mysite import views
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    #최고관리자
    url(r'^admin/', admin.site.urls),
    #관리자
    # url(r'^manager/', admin_home, name='manager_home'),29번행과 30행이 충돌 된다.(url 매핑
    # url(r'^manager/register/', MangerRegisterView.as_view(), name='manager_register'),
    url(r'^manager/$', admin_home, name='manager_home'),
    url(r'^member/', include(('member.urls','permission_edit'), namespace='member')),
    url(r'^blog/post_list/', include(('notice.urls', 'post_list'), namespace='post')),
    url(r'^blog/post_detail', include(('notice.urls', 'post_detail'), namespace='post')),
    url(r'^blog/post_new', include(('notice.urls', 'post_new'), namespace='post')),

    #사용자
    url(r'^$', home, name='home'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^register/', UserRegisterView.as_view(), name='register'),

    url(r'^accounts/password_change/$', UserPasswordChangeView.as_view(), name='password_change'),
    url(r'^accounts/password_change_done/$', UserPasswordDoneView.as_view(),name='password_change_done'),


    #ajax유저아이디검사
    url(r'^ajax/validate_username/$', views.validate_username, name="validate_username"),
    # text위젯
    # url(r'^djrichtextfield/', include('djrichtextfield.urls'))
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]