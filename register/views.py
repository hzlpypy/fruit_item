from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from register.forms import User, LoginForm
from register.models import UserInfo

li_login = []
li_sess = []


# Create your views here.
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
                        request.session['name'] = name
                        UserInfo.objects.create(uname=name, upwd=pwd, uemail=email)
                        return render(request, 'register/login.html', {'form': f})
                    else:
                        return render(request, 'register/register.html', {'form': f, 'error_verify_judge': '验证码错误'})
                else:
                    return render(request, 'register/register.html', {'form': f, 'error_verify': '请输入验证码'})
            else:
                return render(request, 'register/register.html', {'form': f, 'error_pwd': '两次密码不一致'})
        else:
            a = f.errors
            return render(request, 'register/register.html', {"error": f.errors, "form": f})
    else:
        f = User()
        return render(request, 'register/register.html', {'form': f})


def login(request):
    li_login.append('1')
    if li_sess:
        # return render(request, 'home_page/index.html', {'name': request.session['name']})
        return HttpResponseRedirect('/home/')
    else:
        if request.method == 'POST':
            f = LoginForm(request.POST)
            if f.is_valid():
                name = f.cleaned_data['name']
                if UserInfo.objects.filter(uname=name, upwd=f.cleaned_data['pwd']):
                    request.session['name'] = f.cleaned_data['name']
                    li_sess.append(request.session['name'])
                    return render(request, 'home_page/index.html', {'name': request.session['name']})
                else:
                    return render(request, 'register/login.html', {'error': '密码错误', 'form': f,'li_login':li_login})
            else:
                a = f._errors
                return render(request, 'register/login.html', {'error': f._errors, 'form': f,'li_login':li_login})
        else:
            f = LoginForm()
            return render(request, 'register/login.html', {'form': f,'li_login':li_login})
