from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^run-money-parser/', views.run_money_parser, name='run-money-parser'),
    # url(r'^run-money-parser/', views.run_money_parser, name='run-money-parser'),

    url(r'^(?P<pk>[0-9]+)/run-money-parser/$', views.user_check_money, name='run-money-parser'),
    # url(r'^$', views.home, name='home'),
    url(r'^$', views.home, name='home'),
]


