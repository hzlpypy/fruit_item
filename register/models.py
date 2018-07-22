from django.db import models

# Create your models here.
from django.utils import timezone

from homepage.models import Change,Goodsinfo


class UserInfo(models.Model):
    uname = models.CharField(max_length=32,verbose_name='用户名')
    upwd = models.CharField(max_length=255,verbose_name='密码')
    uemail = models.EmailField(max_length=32,verbose_name='邮箱')
    create_data = models.DateTimeField(u'时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(default=timezone.now)
    email_judge = models.IntegerField(default=0)
    isDelete = models.CharField(max_length=32, default='1')


    class Meta:
        db_table = 'userinfo'


class Joincars(models.Model):
    uname = models.ForeignKey(UserInfo)
    goodsinfo = models.CharField(max_length=100, verbose_name='商品名称',null=True)
    # goods = models.ForeignKey(Goodsinfo,null=True)
    goodsnum = models.CharField(max_length=32, verbose_name='商品个数',null=True)
    goodsprice = models.CharField(max_length=32,verbose_name='商品单价',null=True)
    gtotalprice = models.CharField(max_length=32,verbose_name='商品总价',default='')
    gimg = models.CharField(max_length=255,default='1',verbose_name='商品图片',null=True)
    gcount = models.CharField(max_length=8,verbose_name='商品编码')
    createtime = models.DateTimeField(default=timezone.now)
    is_delete = models.BooleanField(default=False)


    class Meta:
        db_table = 'joincars'
        verbose_name = '购物车商品'
        verbose_name_plural = verbose_name