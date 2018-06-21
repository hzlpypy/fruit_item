from django.db import models

# Create your models here.
from django.utils import timezone


class Address(models.Model):
    recipients = models.CharField(max_length=32, null=True)  # 收件人
    detailed_addrss = models.CharField(max_length=255, null=True)  # 详细地址
    postcode = models.CharField(max_length=32, null=True)  # 邮编
    phone = models.CharField(max_length=11, null=True)  # 电话
    uname = models.CharField(max_length=32)
    create_time = models.DateTimeField(default=timezone.now)
    is_delete = models.CharField(max_length=3,default='1')

    class Meta:
        db_table = 'address'
