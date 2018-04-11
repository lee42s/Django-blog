from django.conf.urls import url,include
from member import views

urlpatterns = [
    url(r'^permission/edit(?P<pk>\d+)/$', views.user_permission_edit, name='permission_edit'),
]