# -*- coding: utf-8 -*-
from userinfos import views

__author__ = 'hzl'
__date__ = '202018/6/14 11:52'

from django.conf.urls import url

urlpatterns = [
    url(r'address', views.address, name='address'),
    url(r'order', views.all_order_form, name='order'),
    url(r'person', views.person_info, name='person'),
]
