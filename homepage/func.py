# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.core.mail import send_mail
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader

from homepage.models import Goodsinfo
from register.models import UserInfo

__author__ = 'hzl'
__date__ = '202018/6/19 10:56'

from django.core.paginator import PageNotAnInteger, EmptyPage


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


def login(func):  ###封装验证登录的装饰器***************重点
    def login_fun(request, *args, **kwargs):
        if request.session.has_key('user_id'):
            return func(request, *args, **kwargs)
        else:
            red = HttpResponseRedirect('/register/jizhu')
            red.set_cookie('url', request.get_full_path())
            url = request.COOKIES.get('url', '')
            return red

    return login_fun


# def list_and_search(sort,fruit_info):
#     if sort == '1':  # 按默认排序
#         searchinfo = Goodsinfo.objects.filter(gtitle__contains=fruit_info).order_by('id')
#         ifygoods = Goodsinfo.objects.filter(gtype__contains=fruit_info).order_by('id')
#         id_active = 'id'
#     elif sort == '2':  # 价格排序
#         searchinfo = Goodsinfo.objects.filter(gtitle__contains=fruit_info).order_by('gprice')
#         ifygoods = Goodsinfo.objects.filter(gtype__contains=fruit_info).order_by('gprice')
#         pri_active = 'gprice'
#     else:
#         searchinfo = Goodsinfo.objects.filter(gtitle__contains=fruit_info).order_by('gsalesvolume')
#         ifygoods = Goodsinfo.objects.filter(gtype__contains=fruit_info).order_by('gsalesvolume')
#         sal_active = 'gsalesvolume'
#     return searchinfo,ifygoods


def email_send(url, username,receive_email):
    html_info = loader.get_template('email_send/email_send.html')
    data = {
        'username': username,
        'url': url
    }
    html_message = html_info.render(context=data)
    send_mail('欢迎您加入天天生鲜', '内容', 'hzl5201314159@163.com', [receive_email], html_message=html_message)

def email_activate(request):
    token = request.GET.get('token')
    id = cache.get(token)
    data = {'id': id}
    if id:
        UserInfo.objects.filter(id=id).update(email_judge=1)
        return render(request,'email_send/eamil_judge.html',context=data)
    else:
        return render(request,'email_send/eamil_judge.html',context=data)