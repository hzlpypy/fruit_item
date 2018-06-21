# -*- coding: utf-8 -*-
from homepage import views

__author__ = 'hzl'
__date__ = '202018/6/9 10:27'
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'add', views.add_goods, name='add_good'),
    url(r'car', views.car, name='car'),
    url(r'shop', views.add_cars, name='addcar'),
    url(r'kk/', views.shopcar, name='shopcar'),  # 购物车系统
    url('change/', views.change_count),
    url(r'pay/', views.pay, name='pay'),  # 付款系统
    url(r'search/', views.search, name='search'),  # 全局搜索功能
    url(r'list/', views.fruit_list, name='list'),  # 商品列表(默认)
    url(r'price/', views.fruit_list2, name='list2'),  # 商品列表(价格)
    url(r'sale/', views.fruit_list3, name='list3')
]
