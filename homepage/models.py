from decimal import Decimal
from django.db import models
import datetime
# Create your models here.
from django.db.models import QuerySet
from django.db.models.fields.files import ImageFieldFile
from django.utils import timezone
from tinymce.models import HTMLField  # 富文本编译器


class Change(models.Model):
    class Meta:
        abstract = True

    def to_dict(self):
        dic = {}
        s = vars(self).keys()
        for key in vars(self).keys():
            if not key.startswith('_'):
                things = getattr(self, key)
                if isinstance(things, datetime.datetime):
                    dic[key] = datetime.datetime.strftime(things, '%Y%m%d %H%M%S')
                elif isinstance(things, datetime.date):
                    dic[key] = datetime.datetime.strftime(things, '%Y%m%d ')
                elif isinstance(things, Decimal):
                    dic[key] = float(things)
                elif isinstance(things, ImageFieldFile):
                    dic[key] = str(things)
                else:
                    dic[key] = things
        return dic

    @staticmethod
    def qs_to_dict(qs=None):
        li = []
        if isinstance(qs, QuerySet):
            li = [models.to_dict() for models in qs]
        return li


class Typeinfo(Change):
    title = models.CharField(max_length=64, verbose_name='商品分类')
    judgefruit = models.CharField(max_length=32, default='1')
    banner = models.ImageField(verbose_name='背景图', default='1', upload_to='banner/%Y/%m/')
    createtime = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    isDelete = models.CharField(max_length=1, default='1')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'typeinfo'
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name


class Goodsinfo(Change):
    gid = models.ForeignKey('Typeinfo')
    gtitle = models.CharField(max_length=64, verbose_name='小商品标题')
    gtype = models.CharField(max_length=64, verbose_name='商品类别')
    gprice = models.DecimalField(max_digits=5,decimal_places=2,verbose_name='商品价格')
    gimg = models.ImageField(verbose_name='图片', upload_to='uploads/%Y/%m/', default='1')
    ginfo = models.CharField(max_length=255, verbose_name='商品介绍', default='1')
    gdetailed = HTMLField(default='1') ### 商品介绍
    gcommon = HTMLField(default='1') ### 商品评论
    gsalesvolume = models.IntegerField(max_length=255,verbose_name='销量',default='1')
    gevaluate = models.CharField(max_length=255, verbose_name='商品评论', default='1')
    addtime = models.DateField(default=timezone.now, verbose_name='创建时间')
    a_updatetime = models.DateTimeField(default=timezone.now, verbose_name='更新时间')
    isDelete = models.CharField(max_length=1, default='1')

    def __str__(self):
        return self.gtitle

    class Meta:
        ordering = ['-addtime']
        db_table = 'goodsinfo'
        verbose_name = '小商品信息'
        verbose_name_plural = verbose_name


class Smallinfo(Change):
    sid = models.ForeignKey('Typeinfo')
    infoname = models.CharField(max_length=32, verbose_name='水果小标题')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    is_delete = models.CharField(max_length=3, default='1')

    def __str__(self):
        return self.infoname

    class Meta:
        db_table = 'small_info'
        verbose_name = '水果小分类'
        verbose_name_plural = verbose_name


