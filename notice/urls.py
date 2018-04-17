from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.post_list,name='post_list'),
    url(r'^detail/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),

    url(r'^category_list$', views.notice_category_manager, name='category_list'),
]