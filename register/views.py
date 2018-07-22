import uuid

import requests
# from django.core.cache import cache
from django.core.cache import cache

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# from django_redis import cache
from django.views import View

from homepage.func import email_send
from register.forms import User, LoginForm
from register.models import UserInfo
from hashlib import sha1

li_login = []


# Create your views here.
def fun_pwd(pwd):
    ### 将用户输入的密码转成sha1的加密模式,与数据库中的密码进行判断###
    encrip_pwd = sha1()
    encrip_pwd.update(pwd.encode('utf8'))
    change_pwd = encrip_pwd.hexdigest()
    return change_pwd


######注册#######
def register(request):
    if request.method == 'POST':
        f = User(request.POST)
        if f.is_valid():
            name = f.cleaned_data['name']
            pwd = f.cleaned_data['pwd']
            aginpwd = f.cleaned_data['aginpwd']
            email = f.cleaned_data['email']
            if pwd == aginpwd:  # 判断两次密码输入是否相同
                verify = request.POST.get('info')
                if UserInfo.objects.filter(uname=name):
                    return render(request, 'register/register.html', {'form': f, 'error_user': '用户名已存在'})
                elif UserInfo.objects.filter(uemail=email):
                    return render(request, 'register/register.html', {'form': f, 'error_email': '邮箱已被注册'})
                elif verify:
                    if request.session['verifycode'] == verify.upper():  # 判断验证码是否正确
                        encrypt_pwd = sha1()
                        encrypt_pwd.update(aginpwd.encode('utf8'))
                        new_pwd = encrypt_pwd.hexdigest()
                        user = UserInfo.objects.create(uname=name, upwd=new_pwd, uemail=email)
                        email_token = str(uuid.uuid4())
                        cache.set(email_token,user.id ,timeout=60 * 60 * 24 * 1)
                        URL = request.META.get('REMOTE_ADDR') + '/register/activate?token=' + email_token
                        email_send(URL,name ,email)
                        return HttpResponseRedirect('/register/login')
                    else:
                        return render(request, 'register/register.html', {'form': f, 'error_verify_judge': '验证码错误'})
                else:
                    return render(request, 'register/register.html', {'form': f, 'error_verify': '请输入验证码'})
            else:
                return render(request, 'register/register.html', {'form': f, 'error_pwd': '两次密码不一致'})
        else:
            return render(request, 'register/register.html', {"error": f.errors, "form": f})
    else:
        f = User()
        return render(request, 'register/register.html', {'form': f})


#####登录######
def login(request):
    li_login.append('1')
    if request.method == 'POST':
        f = LoginForm(request.POST)
        jizhu = request.POST.get('jizhu', 0)
        if f.is_valid():
            name = f.cleaned_data['name']
            users = UserInfo.objects.filter(uname=name, upwd=fun_pwd(f.cleaned_data['pwd']))
            if users:
                if users[0].email_judge:
                    if request.session.get('urls', ''):
                        url = request.session.get('urls')
                    else:
                        url = request.COOKIES.get('url', '/home')
                    uname = f.cleaned_data['name']
                    red = HttpResponseRedirect(url)
                    if jizhu != 0:
                        red.set_cookie('uname', uname)  # 通过COOKIE 方式保存信息
                    else:
                        red.set_cookie('uname', '', max_age=-1)
                    token = str(uuid.uuid4())
                    user_id = str(users[0].id)
                    cache.set('user' + user_id, token, timeout=60 * 60 * 2)
                    id = cache.get('user' + user_id, None)
                    request.session['name'] = uname
                    request.session['user_id'] = users[0].id
                    return red
                else:
                    return render(request, 'register/login.html', {'error': '账户未激活', 'form': f, 'li_login': li_login})
            else:
                return render(request, 'register/login.html', {'error': '密码错误', 'form': f, 'li_login': li_login})
        else:
            a = f._errors
            return render(request, 'register/login.html', {'error': f._errors, 'form': f, 'li_login': li_login})
    else:
        f = LoginForm()
        return render(request, 'register/login.html', {'form': f, 'li_login': li_login, 'title': '-登录'})


####记住用户名######3
def jizhu_login(request):
    f = LoginForm()
    uname = request.COOKIES.get('uname', '')
    # if 'name' in request.session:
    #     name = request.session['name']
    return HttpResponseRedirect('/register/login')


######登出#########
def logout(request):
    # del request.session['name']  #### 删除会话
    # del request.session['user_id']
    # s = requests.session()
    # s.get('http://127.0.0.1:8000/home/')
    # s.cookies.clear()
    # request.session.clear()
    request.session.flush()
    red = redirect('/home/')
    red.delete_cookie('goods_ids')  ## 退出时删除相关cookie
    # request.session.set_expiry(0) ###在浏览器关闭时过期
    return red


class UserView(View):
    def get(self):
        pass

    def post(self):
        pass
