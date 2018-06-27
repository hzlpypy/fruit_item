from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

from homepage.models import Goodsinfo
from register.models import Joincars
from userinfos.forms import AddressForm
# Create your views here.
from homepage.views import li_shopcar
from userinfos.models import Address, Lateky
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from homepage import func


@func.login
def address(request):
    li_shopcar.update(a='用户中心')
    name = request.session['name']
    user = Address.objects.filter(uname=name)
    old_phone = ''
    old_detailed_addrss = ''
    old_recipients = ''
    if user:
        dic = model_to_dict(user.first())
        old_phone = dic['phone'][0:3] + '****' + dic['phone'][-4:]  # 电话号码
        old_detailed_addrss = dic['detailed_addrss']  # 详细地址
        old_recipients = dic['recipients']  # 收件人
    if request.method == 'POST':
        f = AddressForm(request.POST)
        if f.is_valid():
            phone = f.cleaned_data['phone']
            recipients = f.cleaned_data['recipients']
            detailed_addrss = f.cleaned_data['detailed_addrss']
            postcode = f.cleaned_data['postcode']
            Address.objects.create(phone=phone, recipients=recipients,
                                   detailed_addrss=detailed_addrss, postcode=postcode,
                                   uname=name)
            return render(request, 'userinfo/address.html', {'shopcar': li_shopcar,
                                                             'form': f, 'success': '添加成功',
                                                             'name': name, 'title': '-首页'})
        else:
            error = f.errors
            context = {'shopcar': li_shopcar, 'form': f, 'error': error,
                       'phone': old_phone, 'recipients': old_recipients, 'detailed_addrss': old_detailed_addrss,
                       'name': name, 'title': '-首页'}
            return render(request, 'userinfo/address.html', context=context)
    else:
        f = AddressForm()
        context = {'shopcar': li_shopcar, 'form': f, 'phone': old_phone, 'recipients': old_recipients,
                   'detailed_addrss': old_detailed_addrss, 'name': name, 'title': '-用户中心'}
        return render(request, 'userinfo/address.html', context=context)


@func.login
def all_order_form(request):
    name = request.session['name']
    li = []
    totalpice = 00.00
    li_shopcar.update(a='用户中心')
    ## 获取购物表数据表中的所有记录
    goods_shop = Joincars.objects.filter(uname=request.session['name'])
    ## 生成paginator对象,定义每页显示3条记录
    paginator = Paginator(goods_shop, 3)
    ## 从前端获取当前页码数,默认为1
    page = request.GET.get('page', 1)
    ## 把当前的页码数转换成整数类型
    currentPage = int(page)
    try:
        goods_shop = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        goods_shop = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第一页的内容
    except EmptyPage:
        # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
        goods_shop = paginator.page(paginator.num_pages)
    for goods_info in goods_shop:
        totalpice += float(model_to_dict(goods_info)['gtotalprice'])
        createtime = model_to_dict(goods_info)['createtime']
        li.append(model_to_dict(goods_info))
    title = '-用户中心'
    return render(request, 'userinfo/order_form.html', locals())


@func.login
def person_info(request):
    dic = {}
    name = request.session['name']
    li_shopcar.update(a='用户中心')
    person = Address.objects.filter(uname=name)
    if person:
        dic = model_to_dict(person.first())
    fruit_id = request.COOKIES.get('goods_ids', '')  # 获取商品浏览的cookie
    fruit_list = []
    recod = Lateky.objects.filter(uname=name)
    if not recod:  ##  如果最开始记录表中没有数据
        if fruit_id:
            Lateky.objects.create(uname=name, info_id=fruit_id)  # 创建数据
            lateky = Lateky.objects.get(uname=name).info_id
            list = lateky.split(',')
            for lately_id in list:
                recently = Goodsinfo.objects.get(id=lately_id)
                fruit_list.append(model_to_dict(recently))
    elif recod and fruit_id:  ###如果最开始有数据,并且cookie中也有数据
        # if recod.first().info_id in fruit_id:  # 判断之前的浏览记录是否与cookie的记录存在重复
        #     old_jilu_id = fruit_id  #  如果有, 则让 cookie记录的fruit_id 直接赋予 old_jilu_id
        # else:  # 如果第一个值不在fruit_id中,则拼接字符串
        #     old_jilu_id = fruit_id + ',' + recod.first().info_id
        # if True:
        #     lack_list = recod.first().info_id.split(',')
        #     for a in fruit_id:
        #         if a:
        #             if lack_list.count(a) >= 1:
        #                 lack_list.remove(fruit_id)
        #             lack_list.insert(0,fruit_id)
        list = fruit_id.split(',')  # 通过逗号,分割字符串,返回一个列表
        lack_list = recod.first().info_id.split(',')
        if len(list) == len(lack_list):
            if len(list) >= 2:
                pass
            Lateky.objects.filter(uname=name).update(info_id=fruit_id)
            for lately_id in list:
                recently = Goodsinfo.objects.get(id=lately_id)
                fruit_list.append(model_to_dict(recently))
        else:
            list_f = fruit_id.split(',')  # 拆分fruit_id 返回一个列表
            for small_id in list_f:
                if lack_list.count(small_id) >= 1:
                    lack_list.remove(small_id)
                a = list_f.index(small_id)
                lack_list.insert(list_f.index(small_id), small_id)
            if len(lack_list) >= 6:
                del lack_list[5:]
            s = ','.join(lack_list)
            Lateky.objects.filter(uname=name).update(info_id=s)
            for lately_id in lack_list:
                recently = Goodsinfo.objects.get(id=lately_id)
                fruit_list.append(model_to_dict(recently))
    else:
        lateky = Lateky.objects.get(uname=name).info_id
        if lateky:
            list = lateky.split(',')
            for lately_id in list:
                recently = Goodsinfo.objects.get(id=lately_id)
                fruit_list.append(model_to_dict(recently))
    return render(request, 'userinfo/person_info.html', {'name': name,
                                                         'shopcar': li_shopcar,
                                                         'form': dic, 'title': '-用户中心', 'fruit_list': fruit_list})
