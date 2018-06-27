# -*- coding: utf-8 -*-
from homepage import views
from homepage.views import MySearchView

__author__ = 'hzl'
__date__ = '202018/6/9 10:27'
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'add/', views.add_goods, name='add_good'),
    url(r'car/', views.car, name='car'), #  购物车详情页面
    url(r'shop/', views.add_cars, name='addcar'),
    url(r'kk/', views.shopcar, name='shopcar'),  # 购物车系统
    url('change/', views.change_count),   # 修改
    url(r'pay/', views.pay, name='pay'),  # 付款系统
    # url(r'search(\d+)_(\d+)_(\d+)/$', views.search, name='search'),  # 全局搜索功能 ,(),(),排序类别
    url('list(\d+)_(\d+)_(\d+)/$', views.fruit_list, name='list'),  # 商品列表(默认),分别对应商品类别,(),排序类别
    url(r'^search/',MySearchView())
]
