import json

from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render

from register.views import li_sess
from .models import Typeinfo,Goodsinfo,Change,Smallinfo
# Create your views here.

def index(request):
    li = []
    lis = []
    title = Typeinfo.objects.filter()
    for title_ob in title:
        title_dict = model_to_dict(title_ob)
        li.append(title_dict)
    if li_sess:
        return render(request,'home_page/index.html',{'title_info':li,'name':request.session['name']})
    else:
        return render(request, 'home_page/index.html', {'title_info': li})

def add_goods(request):
    if request.method == 'GET':
        li = []
        result = {}
        titles = Typeinfo.objects.all()
        if titles:
            for title in titles:
                classify = title.smallinfo_set.all()
                goods = title.goodsinfo_set.all()
                title.fruit = Change.qs_to_dict(goods)
                title.classify = Change.qs_to_dict(classify)
                li.append(title.to_dict())
            result.update(statu=200,msg='success',data=li)
            return HttpResponse(json.dumps(result),content_type='Application/json')

def car(request):
    li = []
    if request.method == 'GET':
        id = request.GET.get('id')
        goods = Goodsinfo.objects.filter(id=id)
        if goods:
            context = goods[0]
            if li_sess:
                return render(request, 'func/car.html', {'name': request.session['name'],'form':context})
            else:
                return render(request, 'func/car.html',{'form':context})
    return HttpResponse('呵呵')

def add_cars(request):
    pass