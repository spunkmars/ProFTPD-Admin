#coding=utf-8
from django.db import models
from proftpd.ftpadmin.models.ftpusers import Ftpuser



class Ftpxferstat(models.Model):
    username = models.CharField(max_length=255, null=True)
    file = models.CharField(max_length=255, null=True)
    size = models.BigIntegerField(null=True, default=0, blank=True)
    address_full = models.CharField(max_length=255, null=True)
    address_ip = models.CharField(max_length=255, null=True)
    command = models.CharField(max_length=255, null=True)
    timespent = models.CharField(max_length=255, null=True)
    time = models.CharField(max_length=255, null=True)
    cmd = models.CharField(max_length=255, null=True)
    dunno = models.CharField(max_length=255, null=True)
#    username_id = models.ForeignKey(Ftpuser)

    class Meta:
        db_table = 'ftpxfer_stat'
        ordering = ['-username']
        app_label = 'ftpadmin'

    def __unicode__(self):
        return self.username

    #为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in Ftpxferstat._meta.fields]







