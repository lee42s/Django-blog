from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.manager_post_list,name='manager_post_list'),
    url(r'^detail/(?P<pk>\d+)/$', views.manager_post_detail, name='manager_post_detail'),
]