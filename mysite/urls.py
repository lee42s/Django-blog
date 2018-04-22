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
from notice.views import ajax_word_filtering,ajax_comment_word_filtering
from mysite import views
from notice.models import Notice_category
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    #최고관리자
    url(r'^admin/', admin.site.urls),
    #관리자만
    # url(r'^manager/', admin_home, name='manager_home'),29번행과 30행이 충돌 된다.(url 매핑
    # url(r'^manager/register/', MangerRegisterView.as_view(), name='manager_register'),
    url(r'^manager/$', admin_home, name='manager_home'),
    url(r'^manager/', include(('member.urls','permission_edit'), namespace='member')),
    url(r'^manager/list/', include(('notice.urls', 'category_list'), namespace='m_category_list')),
    url(r'^manager/new/', include(('notice.urls', 'category_new'), namespace='m_category_new')),
    url(r'^manager/', include(('notice.urls', 'category_edit'), namespace='m_category_edit')),
    url(r'^manager/', include(('notice.urls', 'category_remove'), namespace='m_category_remove')),


    #사용자
    url(r'^notice/', include(('notice.urls', 'post_list'), namespace='notice_list')),
    url(r'^notice/post_detail/', include(('notice.urls', 'post_detail'), namespace='notice_detail')),
    url(r'^notice/post_list/', include(('notice.urls', 'post_new'), namespace='notice_new')),
    url(r'^notice/', include(('notice.urls', 'post_edit'), namespace='notice_edit')),
    url(r'^notice/', include(('notice.urls', 'post_remove'), namespace='notice_remove')),
    url(r'^ajax_comment_edit/', include(('notice.urls', 'comment_edit'), namespace='notice_comment_edit')),
    url(r'^word_filtering/', include(('notice.urls', 'word_filtering'), namespace='word_filtering_manager')),
    url(r'^$', home, name='home'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    # 로그인 페이지에서 각카테고리(gnb)나오기 위해서는 extra_context 을사용하여 카테고리퀘리셋 을적용한다
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'registration/login.html',
                                                 'extra_context':{'category': Notice_category.objects.all()}}, name='login'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^register/', UserRegisterView.as_view(), name='register'),
    url(r'^accounts/password_change/$', UserPasswordChangeView.as_view(), name='password_change'),
    url(r'^accounts/password_change_done/$', UserPasswordDoneView.as_view(),name='password_change_done'),

    url(r'^ajax/validate_content/$', ajax_word_filtering, name="validate_content"),
    url(r'^ajax/validate_comment/$', ajax_comment_word_filtering, name="validate_comment"),



    #ajax유저아이디검사
    url(r'^ajax/validate_username/$', views.validate_username, name="validate_username"),
    # text위젯
    # url(r'^djrichtextfield/', include('djrichtextfield.urls'))
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]