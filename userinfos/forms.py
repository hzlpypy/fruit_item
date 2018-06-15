# -*- coding: utf-8 -*-
from userinfos import models

__author__ = 'hzl'
__date__ = '202018/6/14 11:52'

from django import forms

class AddressForm(forms.Form):
    recipients = forms.CharField(required=True,max_length=32,error_messages={'required':'收件人不能为空'})
    detailed_addrss = forms.CharField(required=True,max_length=255,error_messages={'required':'详细地址不能为空'},
                                      widget=forms.Textarea(attrs={'class':'site_area'}))
    postcode = forms.CharField(required=True,max_length=32,error_messages={'required':'邮编不能为空'})
    phone = forms.CharField(required=True,error_messages={'required':'手机不能为空'},max_length=11)
    # class Meta:
    #     model = models.Address
    #     fields = ['recipients', 'detailed_addrss', 'postcode', 'phone']

