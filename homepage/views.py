import json
from time import sleep

from django.core.cache import cache
from django.template import loader
from django.views.decorators.cache import cache_page

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


#########主页面###########
def index(request):

    li = []
    title = Typeinfo.objects.filter()
    ip = request.META.get('REMOTE_ADDR')
    result = cache.get(ip + 'index', '')
    if result:
        return HttpResponse(result)
    for title_ob in title:
        title_dict = model_to_dict(title_ob)
        li.append(title_dict)
    s = request.session.get('name')
    sleep(0.5)
    context = {'title_info': li, 'title': '-首页'}
    temp = loader.get_template('home_page/index.html')
    result = temp.render(context=context)
    cache.set(ip + 'index', result)
    red = HttpResponse(result)
    return red


########  商品列表 #####################
@cache_page(30)
def fruit_list(request, id, pindex, sort):  # id表示商品类别,例如0代表全部,1代表新鲜水果..sort是按什么类别来排序
    if request.method == 'GET':
        # sleep(2)
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
                   'sal_active': sal_active, 'id': id, 'dic_classify': dic_classify, 'list': list}
        return render(request, 'func/fruit_list.html', context=context)


####购买详情界面######
def car(request):
    li = []
    if request.method == 'GET':
        dic_search = {'a': 1}
        id = request.GET.get('id')
        goods = Goodsinfo.objects.get(id=id)  ###通过id获取下面类别
        fruit_info = Goodsinfo.objects.all().order_by('id')  ### 对id进行排序,下面取最后两个
        #####  获取类别  #####
        new_fruit = model_to_dict(goods)
        ss = new_fruit.get('gid')
        fruit_type = Typeinfo.objects.get(id=ss)
        types = model_to_dict(fruit_type).get('title')
        ######  获取结束 #####
        for two_new_fruit in fruit_info:
            li.append(model_to_dict(two_new_fruit))
        order_li = li[-2:]
        red = render(request, 'func/car.html',
                     {'form': goods, 'order_li': order_li, 'dic_search': dic_search, 'types': types, 'id': ss})

        #############最近浏览判断##############

        goods_ids = request.COOKIES.get('goods_ids', '')  # 获取cookie中的goods_ids
        goods_id = str(goods.id)
        if goods_ids:
            goods_ids1 = goods_ids.split(',')  # 将goods_ids通过逗号切割,返回一个列表
            if goods_ids1.count(goods_id) >= 1:  # 判断goods_id是否存在与goods_ids1中,也就是判断是点击的浏览记录是否重复
                goods_ids1.remove(goods_id)  # 重复就删除
            goods_ids1.insert(0, goods_id)  # 将最新的记录插在索引为0位置,即达到最新展示的目的
            if len(goods_ids1) >= 6:  # 判断是记录列表是否大于5,控制记录显示的条数
                del goods_ids1[5]  # 大于等于6,就删除最后一条
            goods_ids = ','.join(goods_ids1)  ### 用逗号拼接成用逗号相连的字符串
        else:
            goods_ids = goods_id
        red.set_cookie('goods_ids', goods_ids)
        request.session['urls'] = request.get_full_path()
        return red
    return HttpResponse('呵呵')


#####  添加到购物车########
def add_cars(request):
    if 'name' in request.session:
        count = request.POST.get('count')  # 个数
        unitprice = request.POST.get('unitprice')  # 单价
        totalprice = request.POST.get('totalprice')  # 总价
        title = request.POST.get('title')  # 商品名称
        img = request.POST.get('img')  # 图片
        id = request.session['user_id']
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
            Joincars.objects.create(uname_id=id,
                                    goodsinfo=title,
                                    goodsnum=count,
                                    goodsprice=unitprice,
                                    gtotalprice=totalprice,
                                    gimg=img)
            return JsonResponse({'res': 1})
    else:
        red = JsonResponse({'res': 0})
        # red.set_cookie('url', request.get_full_path())
        # a = request.path
        # b = request.get_full_path()
        # url = request.COOKIES.get('url', '')
        return JsonResponse({'res': 0})


#####购物车系统##########
@func.login
def shopcar(request):
    li = []
    if request.method == 'GET':
        dell_id = request.GET.get('id')
        if dell_id:
            Joincars.objects.filter(uname_id=request.session.get('user_id'), id=dell_id).delete()
        user = UserInfo.objects.get(id=request.session.get('user_id'))
        info = user.joincars_set.all()
        # info = Joincars.objects.filter(uname_id=request.session.get('user_id'))
        li_shopcar.update(a='购物车')
        i = 0
        if info:
            for shopcarinfo in info:
                i += 1
                ### 在这进行删除判断,通过isdelete ###
                if shopcarinfo.is_delete == 1:
                    pass
        return render(request, 'func/shopcar.html', {'shopcar': li_shopcar, 'form': info, 'i': i})


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
        user_id = request.session['user_id']
        user_shop = Joincars.objects.filter(uname_id=user_id)
        for info in user_shop:
            i += 1
            dic = model_to_dict(info).get('goodsinfo')
            Joincars.objects.filter(uname_id=user_id, goodsinfo=dic).update(gcount=i)
            li.append(model_to_dict(info))
            dic_money = float(model_to_dict(info).get('gtotalprice'))
            li_price += dic_money
        reality_price = li_price + 10
        return render(request, 'func/pay_money.html',
                      {'shopcar': li_shopcar, 'form': li, 'i': i, 'totalprice': str(li_price)[0:6],
                       'reality_price': str(reality_price)[0:6]})


from haystack.views import SearchView


##### 搜索HTML文件 ####
#    <div class="navbar_con">
#         <div class="navbar clearfix">
#             <div class="subnav_con fl">
#                 <h1>全部商品分类</h1>
#                 <span></span>
#                 <ul class="subnav">
#                     <li><a href="#" class="fruit">新鲜水果</a></li>
#                     <li><a href="#" class="seafood">海鲜水产</a></li>
#                     <li><a href="#" class="meet">猪牛羊肉</a></li>
#                     <li><a href="#" class="egg">禽类蛋品</a></li>
#                     <li><a href="#" class="vegetables">新鲜蔬菜</a></li>
#                     <li><a href="#" class="ice">速冻食品</a></li>
#                 </ul>
#             </div>
#             <ul class="navlist fl">
#                 <li><a href="{% url 'index' %}">首页</a></li>
#                 <li class="interval">|</li>
#                 <li><a href="">手机生鲜</a></li>
#                 <li class="interval">|</li>
#                 <li><a href="">抽奖</a></li>
#             </ul>
#         </div>
#     </div>
#
# {% if searchinfo.has_previous %}
#                     <!-- 当前页的上一页按钮正常使用-->
#                     <li class="previous"><a
#                             href="/search/?info={{ info }}&&page={{ searchinfo.previous_page_number }}">上一页</a>
#                     </li>
#                 {% elif ifygoods.has_previous %}
#                     <li class="previous"><a
#                             href="/search/?info={{ info }}&&page={{ ifygoods.previous_page_number }}">上一页</a>
#                     </li>
#                 {% else %}
#                     <!-- 当前页的不存在上一页时,上一页的按钮不可用-->
#                     <li class="previous disabled"><a href="#">上一页</a></li>
#                 {% endif %}
#                 <!-- 上一页按钮结束 -->
#                 <!-- 页码开始 -->
#                 {% for num in paginator.page_range %}
#                     {% if num ==  currentPage %}
#                         <li class="item active"><a href="search/?info={{ info }}&&page={{ num }}">{{ num }}</a>
#                         </li>
#                     {% else %}
#                         <li class="item"><a href="search/?info={{ info }}&&page={{ num }}">{{ num }}</a></li>
#                     {% endif %}
#                 {% endfor %}
#                 <!-- 页码结束 -->
#                 <!--下一页按钮开始 -->
#                 {% if searchinfo.has_next %}
#                     <li class="next"><a
#                             href="search/?info={{ info }}&&page={{ searchinfo.next_page_number }}">下一页</a>
#                     </li>
#                 {% elif ifygoods.has_next %}
#                     <li class="next"><a
#                             href="search/?info={{ info }}&&page={{ ifygoods.next_page_number }}">下一页</a>
#                     </li>
#                 {% else %}
#                     <li class="next disabled"><a href="#">下一页</a></li>
#                 {% endif %}


class MySearchView(SearchView):
    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        context['title'] = '-搜索'
        context['dic_search'] = 1
        context['newfruit'] = news()
        return context
