from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/', views.register_user, name='register_user'),
    url(r'^(?P<pk>[0-9]+)/$', views.user_detail, name='user_detail'),
    url(r'^pr/', views.pr, name='profile'),
]


