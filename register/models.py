from django.db import models

# Create your models here.
from django.utils import timezone

from homepage.models import Change


class UserInfo(models.Model):
    uname = models.CharField(max_length=32,verbose_name='用户名')
    upwd = models.CharField(max_length=32,verbose_name='密码')
    uemail = models.EmailField(max_length=32,verbose_name='邮箱')
    create_data = models.DateTimeField(u'时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(default=timezone.now)
    isDelete = models.CharField(max_length=32, default='1')

    class Meta:
        db_table = 'userinfo'


class Joincars(models.Model):
    uname = models.CharField(max_length=32,verbose_name='用户名',default='1')
    goodsinfo = models.CharField(max_length=100, verbose_name='商品名称')
    goodsnum = models.CharField(max_length=32, verbose_name='商品个数')
    goodsprice = models.CharField(max_length=32,verbose_name='商品单价')
    gtotalprice = models.CharField(max_length=32,verbose_name='商品总价')
    gimg = models.CharField(max_length=255,default='1',verbose_name='商品图片')
    gcount = models.CharField(max_length=8,verbose_name='商品编码')
    createtime = models.DateTimeField(default=timezone.now)
    is_delete = models.CharField(max_length=32,default='1')

    def __str__(self):
        return self.goodsinfo

    class Meta:
        db_table = 'joincars'
        verbose_name = '购物车商品'
        verbose_name_plural = verbose_name