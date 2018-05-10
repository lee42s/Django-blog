from django.conf.urls import url

from . import views

urlpatterns = [
    #사용자
    url(r'^list/categroy(?P<category>\d+)/$', views.post_list, name='post_list'),
    url(r'^detail/(?P<pk>\d+)/categroy(?P<category>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^new/categroy(?P<category>\d+)/$', views.post_new, name='post_new'),
    url(r'^edit/(?P<pk>\d+)/categroy(?P<category>\d+)/$', views.post_edit,  name='post_edit'),
    url(r'remove/(?P<pk>\d+)/categroy(?P<category>\d+)/$', views.post_remove, name='post_remove'),
    url(r'remove/comment(?P<comment_pk>\d+)/post(?P<pk>\d+)/categroy(?P<category>\d+)/$', views.comment_remove, name='comment_remove'),
    url(r'remove/imges(?P<imge_pk>\d+)/post(?P<pk>\d+)/categroy(?P<category>\d+)/$', views.imges_remove, name='imges_remove'),
    url(r'remove/files(?P<file_pk>\d+)/post(?P<pk>\d+)/categroy(?P<category>\d+)/$', views.files_remove, name='files_remove'),



    #관리자
    url(r'^category_list$', views.notice_category_manager, name='category_list'),
    url(r'^category/new$', views.new_notice_category_manager, name='category_new'),
    url(r'^category/edit(?P<pk>\d+)/$', views.notice_category_edit, name='category_edit'),
    url(r'category/(?P<pk>\d+)/remove/$', views.notice_category_remove, name='category_remove'),
    url(r'^word_filtering/$', views.word_filtering, name='word_filtering'),
]