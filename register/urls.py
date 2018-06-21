# -*- coding: utf-8 -*-
from register import views, verifycode

__author__ = 'hzl'
__date__ = '202018/6/7 18:00'
from django.conf.urls import url

urlpatterns = [
    url('register/', views.register, name='reg'),
    url('login/', views.login, name='login'),
    url('verify/', verifycode.verifycode, name='verify'),
    url('jizhu/', views.jizhu_login, name='jizhu'),
]
