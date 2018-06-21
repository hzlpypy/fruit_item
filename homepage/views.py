import json
from homepage.func import fun, news

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from register.models import Joincars, UserInfo

from .models import Typeinfo, Goodsinfo, Change, Smallinfo

# Create your views here.
li_shopcar = {}  # 判断前端头部界面是否为购物车,或者支付界面,或者用户中心界面


#########主页面###########
def index(request):
    li = []
    title = Typeinfo.objects.filter()
    for title_ob in title:
        title_dict = model_to_dict(title_ob)
        li.append(title_dict)
    s = request.COOKIES
    try:
        name = request.session['name']
        if name:
            return render(request, 'home_page/index.html', {'title_info': li, 'name': name})
    except:
        return render(request, 'home_page/index.html', {'title_info': li})


##########搜索################
def search(request):
    if request.method == 'GET':
        li = []
        dic_search = {'a': 1}
        info = request.GET.get('info')
        # 获取关于搜索关键字的所有数据
        searchinfo = Goodsinfo.objects.filter(gtitle__contains=info)
        ifygoods = Goodsinfo.objects.filter(gtype__contains=info)
        # 生成paginator对象, 定义每页显示6条记录
        # paginator = Paginator(searchinfo,3)
        # 从前端获取当前页码数,默认为1
        page = request.GET.get('page', 1)
        # 把当前的页码数转换成整数类型
        # currentPage = int(page)
        # try:
        #     searchinfo = paginator.page(page)
        # except PageNotAnInteger:
        #     searchinfo = paginator.page(1)
        # except EmptyPage:
        #     searchinfo = paginator.page(paginator.num_pages)
        if searchinfo:
            paginator = Paginator(searchinfo, 2)
            fun(page, paginator)
            for goodsinfo in searchinfo:
                li.append(model_to_dict(goodsinfo))
        elif ifygoods:
            paginator = Paginator(ifygoods, 2)
            fun(page, paginator)
            for goodsinfo in ifygoods:
                li.append(model_to_dict(goodsinfo))
        if 'name' in request.session:
            name = request.session['name']
    return render(request, 'func/search.html', locals())


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


########  商品列表(默认) #####################
def fruit_list(request):
    if request.method == 'GET':
        li = []
        new_fruit_li = []
        dic_search = {'a': 1}
        fruit_info = Goodsinfo.objects.all().order_by('id')
        paginator = Paginator(fruit_info, 10)
        page = request.GET.get('page', 1)
        s = fun(page, paginator)
        for info in s:
            dic = model_to_dict(info)
            li.append(dic)
        if 'name' in request.session:
            name = request.session['name']
            context = {'dic_search': dic_search, 'info': li, 'name': name,
                       'paginator': paginator, 'fruit_info': fruit_info, 's': s, 'newfruit': news()}
        else:
            context = {'dic_search': dic_search, 'info': li, 's': s,'paginator': paginator, 'fruit_info': fruit_info,'newfruit': news()}
        return render(request, 'func/fruit_list.html', context=context)


########  商品列表(价格) #####################
def fruit_list2(request):
    li = []
    dic_search = {'a': 1}
    fruit_info = Goodsinfo.objects.order_by('gprice')
    paginator = Paginator(fruit_info, 10)
    page = request.GET.get('page', 1)
    s = fun(page, paginator)
    for info in s:
        dic = model_to_dict(info)
        li.append(dic)
    if 'name' in request.session:
        name = request.session['name']
        context = {'dic_search': dic_search, 'info': li, 'name': name,
                   'paginator': paginator, 'fruit_info': fruit_info, 's': s, 'newfruit': news()}
    else:
        context = {'dic_search': dic_search, 'info': li, 's': s}
    return render(request, 'func/fruit_list2.html', context=context)


########  商品列表(人气----销量) #####################
def fruit_list3(request):
    li = []
    dic_search = {'a': 1}
    fruit_info = Goodsinfo.objects.order_by('gsalesvolume')
    paginator = Paginator(fruit_info, 10)
    page = request.GET.get('page', 1)
    s = fun(page, paginator)
    for info in s:
        dic = model_to_dict(info)
        li.append(dic)
    if 'name' in request.session:
        name = request.session['name']
        context = {'dic_search': dic_search, 'info': li, 'name': name,
                   'paginator': paginator, 'fruit_info': fruit_info, 's': s, 'newfruit': news()}

    else:
        context = {'dic_search': dic_search, 'info': li, 's': s}
    return render(request, 'func/fruit_list3.html', context=context)


####购买详情界面######
def car(request):
    li = []
    if request.method == 'GET':
        id = request.GET.get('id')
        goods = Goodsinfo.objects.filter(id=id)
        if goods:
            context = goods[0]
            if 'name' in request.session:
                name = request.session['name']
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
        if 'name' in request.session:
            name = request.session['name']
            if Joincars.objects.filter(goodsinfo=title):
                judge_num = unitprice.split('.')
                if len(judge_num) > 0:  # 判断是否为浮点型和整形  大于0为浮点型 否则反之
                    Joincars.objects.filter(goodsinfo=title).update(goodsnum=F('goodsnum') + int(count),
                                                                    gtotalprice=F('gtotalprice') + (
                                                                            int(count) * float(unitprice)),
                                                                    is_delete='1')
                else:
                    Joincars.objects.filter(goodsinfo=title).update(goodsnum=F('goodsnum') + int(count),
                                                                    gtotalprice=F('gtotalprice') + (
                                                                            int(count) * int(unitprice)))
                return JsonResponse({'res': 1})
            else:
                Joincars.objects.create(uname=name,
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


#####购物车系统##########
def shopcar(request):
    li = []
    if request.method == 'GET':
        dell_id = request.GET.get('id')
        if 'name' in request.session:
            name = request.session['name']
            if dell_id:
                Joincars.objects.filter(uname=name, id=dell_id).delete()
            info = Joincars.objects.filter(uname=name)
            li_shopcar.update(a='购物车')
            i = 0
            if info:
                for shopcarinfo in info:
                    i += 1
                    fruits = model_to_dict(shopcarinfo)
                    ### 在这进行删除判断,通过isdelete ###
                    if fruits['is_delete'] == '1':
                        shop_dict = fruits
                        li.append(shop_dict)
            return render(request, 'func/shopcar.html', {'shopcar': li_shopcar, 'form': li, 'name': name, 'i': i})
        else:
            # return JsonResponse({'res': 1})
            return HttpResponseRedirect('/register/login')
    pass


######前端点击修改商数量时,购物车数据库数据跟着修改#############
def change_count(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        count = request.GET.get('count')
        user = Joincars.objects.filter(id=id)
        if int(count) > 0 and int(count) < 100:
            if user:
                oldcount = model_to_dict(user[0])['goodsnum']
                oneprice = model_to_dict(user[0])['goodsprice']
                judge_num = oneprice.split('.')
                if len(judge_num) > 0:  # 判断是否为浮点型
                    Joincars.objects.filter(id=id).update(goodsnum=count, gtotalprice=float(oneprice) * int(count))
                else:
                    Joincars.objects.filter(id=id).update(goodsnum=count, gtotalprice=int(oneprice) * int(count))
                return JsonResponse({'res': oldcount})
        else:
            pass


#########点击支付界面####################
def pay(request):
    if request.method == 'GET':
        li_shopcar.update(a='提交订单')
        li = []
        li_price = 0
        i = 0
        if 'name' in request.session:
            name = request.session['name']
            user_shop = Joincars.objects.filter(uname=name)
            for info in user_shop:
                i += 1
                dic = model_to_dict(info).get('goodsinfo')
                Joincars.objects.filter(uname=name, goodsinfo=dic).update(gcount=i)
                li.append(model_to_dict(info))
                dic_money = float(model_to_dict(info).get('gtotalprice'))
                li_price += dic_money
            reality_price = li_price + 10
            return render(request, 'func/pay_money.html',
                          {'shopcar': li_shopcar, 'form': li, 'i': i, 'totalprice': str(li_price)[0:6],
                           'reality_price': str(reality_price)[0:6], 'name': name})
