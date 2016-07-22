from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^register/', views.register_user, name='register_user'),
    # url(r'^login/', views.user_login, name='user_login'),
    # url(r'^logout/', views.user_logout, name='user_logout'),
    url(r'^admin/readd-all-commits', views.readd_all_commits, name='readd_all_commits'),
    url(r'^admin/readd-all-news-wed', views.readd_all_news_wed, name='readd_all_news_wed'),
    # url(r'^all', views.all_news, name='all_news'),
    url(r'^(?P<news_type>[\w-]+)/$', views.all_news, name='all_news'),
    # url(r'^(?P<pk>[0-9]+)/$', views.user_detail, name='user_detail'),
    # url(r'^(?P<pk>[0-9]+)/preferences/$', views.user_preferences, name='user_detail'),
    # url(r'^', views.home, name='home'),

]


