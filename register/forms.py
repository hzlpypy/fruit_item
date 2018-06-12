# -*- coding: utf-8 -*-
__author__ = 'hzl'
__date__ = '202018/6/7 18:00'

from django import forms
from register.models import UserInfo


class User(forms.Form):
    name = forms.CharField(label='用户名', required=True, max_length=32, error_messages={'required': '请输入用户名'})
    pwd = forms.CharField(required=True, min_length=6, max_length=32, error_messages={'required': '请输入密码'}, label='密码')
    aginpwd = forms.CharField(required=True, min_length=6, max_length=32, error_messages={'required': '请输入确认密码'},
                              label='再次输入密码')
    email = forms.EmailField(required=True, error_messages={'required': '邮箱不能为空'})

    def clean(self):
        # 用户名
        try:
            email = self.cleaned_data['email']
        except:
            raise forms.ValidationError(u'注册账号需为邮箱格式')
        try:
            pwd = self.cleaned_data['pwd']
        except:
            raise forms.ValidationError(u'密码过短,请输入至少6位数密码')
        try:
            aginpwd = self.cleaned_data['aginpwd']
        except:
            raise forms.ValidationError(u'密码过短,请输入至少6位数密码')
        return self.cleaned_data

class LoginForm(forms.Form):
    name = forms.CharField(required=True,min_length=3,max_length=24,
                           error_messages={'required':'请输入用户名'},
                           widget=forms.TextInput(attrs={'class':'name_input','placeholder':'请输入用户名'}))
    pwd = forms.CharField(required=True,min_length=3,max_length=32,error_messages={'required':'请输入密码'},
                          widget=forms.TextInput(attrs={'class':'pass_input','placeholder':'请输入密码'}))

    def clean(self):
        try:
            pwd = self.cleaned_data['pwd']
        except:
            raise forms.ValidationError('密码格式不正确')
        return self.cleaned_data
        # name = self.cleaned_data['name']
        # password = self.cleaned_data['pwd']
        # judge = UserInfo.objects.filter(uname=name,upwd=password)
        # if judge:
        #     pass
        # else:
        #     raise forms.ValidationError('登录失败,密码错误')
        # return self.cleaned_data