from django.conf.urls import url
from member import views

urlpatterns = [
    # url(r'^$',views.user_permission_list, name='permission'),
    url(r'^permission/edit(?P<pk>\d+)/$', views.user_permission_edit, name='permission_edit'),
]