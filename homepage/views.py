import json
from homepage.func import fun, news

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from register.models import Joincars, UserInfo
from homepage import func
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
            return render(request, 'home_page/index.html', {'title_info': li, 'name': name, 'title': '-首页'})
    except:
        return render(request, 'home_page/index.html', {'title_info': li, 'title': '-首页'})


##########搜索################
def search(request,id,pindex,sort):
    if request.method == 'GET':
        id_active = ''
        pri_active = ''
        sal_active = ''
        info = []
        dic_search = {'a': 1}
        fruit_info = request.GET.get('info')
        # 获取关于搜索关键字的所有数据
        if sort == '1': # 按默认排序
            searchinfo = Goodsinfo.objects.filter(gtitle__contains=fruit_info).order_by('id')
            ifygoods = Goodsinfo.objects.filter(gtype__contains=fruit_info).order_by('id')
            id_active = 'id'
        elif sort == '2': # 价格排序
            searchinfo = Goodsinfo.objects.filter(gtitle__contains=fruit_info).order_by('gprice')
            ifygoods = Goodsinfo.objects.filter(gtype__contains=fruit_info).order_by('gprice')
            pri_active = 'gprice'
        else:
            searchinfo = Goodsinfo.objects.filter(gtitle__contains=fruit_info).order_by('gsalesvolume')
            ifygoods = Goodsinfo.objects.filter(gtype__contains=fruit_info).order_by('gsalesvolume')
            sal_active = 'gsalesvolume'
        page = request.GET.get('page', 1)
        if searchinfo:
            paginator = Paginator(searchinfo, 2)
            fun(page, paginator)
            for goodsinfo in searchinfo:
                info.append(model_to_dict(goodsinfo))
        elif ifygoods:
            paginator = Paginator(ifygoods, 2)
            fun(page, paginator)
            for goodsinfo in ifygoods:
                info.append(model_to_dict(goodsinfo))
        newfruit = news()
    return render(request, 'func/fruit_list.html', locals())


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


########  商品列表 #####################
def fruit_list(request, id, pindex, sort):  # id表示商品类别,例如0代表全部,1代表新鲜水果..sort是按什么类别来排序
    if request.method == 'GET':
        list = '5'
        id_active = ''
        pri_active = ''
        sal_active = ''
        li = []
        dic_search = {'a': 1}
        classifys = Typeinfo.objects.filter(id=id)
        if classifys:
            dic_classify = model_to_dict(classifys.first()).get('title')
        else:
            dic_classify = ''
        if id == '0':  # 表示取全部
            goodsinfo = Goodsinfo.objects.all()
        else:
            typeinfo = Typeinfo.objects.get(id=id)
            goodsinfo = typeinfo.goodsinfo_set.all()
        if sort == '1':  # 按默认排序
            fruit_info = goodsinfo.order_by('id')
            id_active = 'active'
        elif sort == '2':  # 按价格排序
            fruit_info = goodsinfo.order_by('gprice')
            pri_active = 'active'
        else:
            fruit_info = goodsinfo.order_by('gsalesvolume')
            sal_active = 'active'
        paginator = Paginator(fruit_info, 8)
        page = request.GET.get('page', 1)
        s = fun(page, paginator)
        for info in s:
            dic = model_to_dict(info)
            li.append(dic)
        context = {'dic_search': dic_search, 'info': li,
                   'paginator': paginator, 'fruit_info': fruit_info,
                   's': s, 'newfruit': news(), 'url': '/home/list{}_1_{}'.format(id, sort),
                   'id_active': id_active, 'pri_active': pri_active,
                   'sal_active': sal_active, 'id': id, 'dic_classify': dic_classify,'list':list}
        return render(request, 'func/fruit_list.html', context=context)


####购买详情界面######
def car(request):
    li = []
    order_li = []
    if request.method == 'GET':
        dic_search = {'a': 1}
        id = request.GET.get('id')
        goods = Goodsinfo.objects.filter(id=id)  ###通过id获取下面类别
        fruit_info = Goodsinfo.objects.all().order_by('id') ### 对id进行排序,下面取最后两个
        if goods:
            #####  获取类别  #####
            new_fruit = model_to_dict(goods.first())
            ss = new_fruit.get('gid')
            fruit_type = Typeinfo.objects.get(id=ss)
            types = model_to_dict(fruit_type).get('title')
            ######  获取结束 #####
            for two_new_fruit in fruit_info:
                li.append(model_to_dict(two_new_fruit))
            order_li = li[-2:]
            fruits = goods[0]
            return render(request, 'func/car.html', {'form': fruits,'order_li': order_li,'dic_search':dic_search,'types':types,'id':ss})

    return HttpResponse('呵呵')


#####  添加到购物车########
def add_cars(request):
    if 'name' in request.session:
        count = request.POST.get('count')  # 个数
        unitprice = request.POST.get('unitprice')  # 单价
        totalprice = request.POST.get('totalprice')  # 总价
        title = request.POST.get('title')  # 商品名称
        img = request.POST.get('img')  # 图片
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
            # url = request.COOKIES.get('url','/')
            # return HttpResponseRedirect(url)
    else:
        return JsonResponse({'res':0})




#####购物车系统##########
@func.login
def shopcar(request):
    li = []
    if request.method == 'GET':
        dell_id = request.GET.get('id')
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
        return render(request, 'func/shopcar.html', {'shopcar': li_shopcar, 'form': li,'i': i})


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
@func.login
def pay(request):
    if request.method == 'GET':
        li_shopcar.update(a='提交订单')
        li = []
        li_price = 0
        i = 0
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
                       'reality_price': str(reality_price)[0:6]})
