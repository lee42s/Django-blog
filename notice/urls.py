from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.post_list,name='post_list'),
    url(r'^detail/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),

    url(r'^category_list$', views.notice_category_manager, name='category_list'),
    url(r'^category/new$', views.new_notice_category_manager, name='category_new'),
    url(r'^category/edit(?P<pk>\d+)/$', views.notice_category_edit, name='category_edit'),
    url(r'category/(?P<pk>\d+)/remove/$', views.notice_category_remove, name='category_remove'),
]