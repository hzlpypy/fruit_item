import json

from django.db.models import F
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from register.models import Joincars, UserInfo
from register.views import li_sess
from .models import Typeinfo, Goodsinfo, Change, Smallinfo

# Create your views here.
li_shopcar = []


#########主页面##############
def index(request):
    li = []
    lis = []
    title = Typeinfo.objects.filter()
    for title_ob in title:
        title_dict = model_to_dict(title_ob)
        li.append(title_dict)
    if li_sess:
        return render(request, 'home_page/index.html', {'title_info': li, 'name': request.session['name']})
    else:
        return render(request, 'home_page/index.html', {'title_info': li, 'shopcar': li_shopcar})


######### 传递json数据给主页面进行添加水果操作#################
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
            result.update(statu=200, msg='success', data=li)
            return HttpResponse(json.dumps(result), content_type='Application/json')


####购买详情界面######
def car(request):
    li = []
    if request.method == 'GET':
        id = request.GET.get('id')
        goods = Goodsinfo.objects.filter(id=id)
        if goods:
            context = goods[0]
            if li_sess:
                return render(request, 'func/car.html', {'name': request.session['name'],
                                                         'form': context})
            else:
                return render(request, 'func/car.html', {'form': context})
    return HttpResponse('呵呵')


#####  添加到购物车########
def add_cars(request):
    if request.method == 'POST':
        count = request.POST.get('count')  # 个数
        unitprice = request.POST.get('unitprice')  # 单价
        totalprice = request.POST.get('totalprice')  # 总价
        title = request.POST.get('title')  # 商品名称
        img = request.POST.get('img')  # 图片
        if li_sess:
            name = li_sess[0]
            if Joincars.objects.filter(goodsinfo=title):
                judge_num = unitprice.split('.')
                if len(judge_num) > 0:  # 判断是否为浮点型和整形  大于0为浮点型 否则反之
                    Joincars.objects.filter(goodsinfo=title).update(goodsnum=F('goodsnum') + int(count),
                                                                    gtotalprice=F('gtotalprice') + (
                                                                            int(count) * float(unitprice)))
                else:
                    Joincars.objects.filter(goodsinfo=title).update(goodsnum=F('goodsnum') + int(count),
                                                                    gtotalprice=F('gtotalprice') + (
                                                                            int(count) * int(unitprice)))
                return JsonResponse({'res': 1})
            else:
                cars = Joincars.objects.create(uname=name,
                                               goodsinfo=title,
                                               goodsnum=count,
                                               goodsprice=unitprice,
                                               gtotalprice=totalprice,
                                               gimg=img)
                return JsonResponse({'res': 1})
        else:
            return JsonResponse({'res': 0})
    else:
        return JsonResponse({'res': 0})

    ######## 购物车系统#########


#####购物车系统##########
def shopcar(request):
    li = []
    if request.method == 'GET':
        if li_sess:
            name = li_sess[0]
            info = Joincars.objects.filter(uname=name)
            li_shopcar.append(1)
            i = 0
            if info:
                for shopcarinfo in info:
                    i += 1
                    shop_dict = model_to_dict(shopcarinfo)
                    li.append(shop_dict)
            return render(request, 'func/shopcar.html', {'shopcar': li_shopcar, 'form': li, 'name': name, 'i': i})
        else:
            return JsonResponse({'res': 1})
    pass


def change_count(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        user = Joincars.objects.filter(id=id)
        if user:
            count = model_to_dict(user[0])['goodsnum']
            return JsonResponse({'res': count})
        else:
            pass

