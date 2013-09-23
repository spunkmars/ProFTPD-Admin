#coding=utf-8
from django.db import models
from proftpd.ftpadmin.models.ftpusers import Ftpuser
from proftpd.ftpadmin.settings import  QUOTA_CHOICES

class Ftpquotatallies(models.Model):
    username = models.CharField(max_length=255, unique=True)
    quota_type = models.CharField(max_length=255, choices=QUOTA_CHOICES, default='user')
    bytes_in_used = models.FloatField(blank=True, null=True)
    bytes_out_used = models.FloatField(blank=True, null=True)
    bytes_xfer_used = models.FloatField(blank=True, null=True)
    files_in_used = models.BigIntegerField(blank=True, null=True)
    files_out_used = models.BigIntegerField(blank=True, null=True)
    files_xfer_used = models.BigIntegerField(blank=True, null=True)
    username_id = models.ForeignKey(Ftpuser)

    class Meta:
        db_table = 'ftpquotatallies'
        ordering = ['username']
        app_label = 'ftpadmin'



    def __unicode__(self):
        return self.username
    #为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in Ftpquotatallies._meta.fields]
