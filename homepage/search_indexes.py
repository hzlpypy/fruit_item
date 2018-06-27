# -*- coding: utf-8 -*-
from homepage.models import Goodsinfo,Typeinfo

__author__ = 'hzl'
__date__ = '202018/6/25 16:36'
from haystack import indexes
class GoodsInfoIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True)

    def get_model(self):
        return Goodsinfo

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class GoodsTypeIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True)

    def get_model(self):
        return Typeinfo

    def index_queryset(self, using=None):
        return self.get_model().objects.all()