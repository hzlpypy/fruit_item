from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from register.models import Joincars
from userinfos.forms import AddressForm
# Create your views here.
from homepage.views import li_shopcar
from userinfos.models import Address
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from homepage import func


@func.login
def address(request):
    li_shopcar.update(a='用户中心')
    name = request.session['name']
    user = Address.objects.filter().first()
    dic = model_to_dict(user)
    phone = dic['phone'][0:3] + '****' + dic['phone'][-4:]  # 电话号码
    detailed_addrss = dic['detailed_addrss']  # 详细地址
    recipients = dic['recipients']  # 收件人
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
                       'phone': phone, 'recipients': recipients, 'detailed_addrss': detailed_addrss,
                       'name': name, 'title': '-首页'}
            return render(request, 'userinfo/address.html', context=context)
    else:
        f = AddressForm()
        context = {'shopcar': li_shopcar, 'form': f, 'phone': phone, 'recipients': recipients,
                   'detailed_addrss': detailed_addrss, 'name': name, 'title': '-用户中心'}
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
    name = request.session['name']
    li_shopcar.update(a='用户中心')
    person = Address.objects.filter(uname=name).first()
    dic = model_to_dict(person)
    return render(request, 'userinfo/person_info.html', {'name': name,
                                                         'shopcar': li_shopcar,
                                                         'form': dic, 'title': '-用户中心'})

