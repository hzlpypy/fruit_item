# -*- coding: utf-8 -*-
from django.forms import model_to_dict

from homepage.models import Goodsinfo

__author__ = 'hzl'
__date__ = '202018/6/19 10:56'

from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator


def fun(page, paginator):
    currentPage = int(page)
    try:
        info = paginator.page(page)
    except PageNotAnInteger:
        info = paginator.page(1)
    except EmptyPage:
        info = paginator.page(paginator.num_pages)
    s = info.has_next
    return info


def news():
    li_news = []
    for new_info in Goodsinfo.objects.all():
        li_news.append(model_to_dict(new_info))
    two_new_fruit = li_news[-2:]
    return two_new_fruit

