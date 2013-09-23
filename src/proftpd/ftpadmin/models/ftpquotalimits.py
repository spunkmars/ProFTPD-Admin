#coding=utf-8
from django.db import models
from proftpd.ftpadmin.models.ftpusers import Ftpuser
from proftpd.ftpadmin.models.ftpquotatallies import Ftpquotatallies
from proftpd.ftpadmin import signals
from proftpd.ftpadmin.settings import QUOTA_CHOICES, SESSION_CHOICES, LIMIT_CHOICES, LIMIT_DEFAULT_VALUE



class Ftpquotalimits(models.Model):
    username_id = models.ForeignKey(Ftpuser, verbose_name="username")
    username = models.CharField(max_length=255,  blank=True, null=True, editable=False, unique=True)
    quota_type = models.CharField(max_length=255, choices=QUOTA_CHOICES, default='user')
    per_session = models.CharField(max_length=255, choices=SESSION_CHOICES, default='false')
    limit_type = models.CharField(max_length=255, choices=LIMIT_CHOICES, default='hard')
    bytes_in_avail = models.FloatField(default=LIMIT_DEFAULT_VALUE['bytes_in_avail'])
    bytes_out_avail = models.FloatField(default=LIMIT_DEFAULT_VALUE['bytes_out_avail'])
    bytes_xfer_avail = models.FloatField(default=LIMIT_DEFAULT_VALUE['bytes_xfer_avail'])
    files_in_avail = models.BigIntegerField(default=LIMIT_DEFAULT_VALUE['files_in_avail'])
    files_out_avail  = models.BigIntegerField(default=LIMIT_DEFAULT_VALUE['files_out_avail'])
    files_xfer_avail = models.BigIntegerField(default=LIMIT_DEFAULT_VALUE['files_xfer_avail'])


    class Meta:
        db_table = 'ftpquotalimits'
        ordering = ['username']
        app_label = 'ftpadmin'


    def __unicode__(self):
        return self.username

    #为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in Ftpquotalimits._meta.fields]

    def delete(self, *args, **kwargs):
        signals.delete_ftpquotalimits_done.send(sender=Ftpquotalimits, obj=self)
        super(Ftpquotalimits, self).delete(*args, **kwargs)


    def save(self, *args, **kwargs):
        first_create = 0
        if self.id is None:
            first_create = 1
        else:
            ftpquotalimits = Ftpquotalimits.objects.get(pk=self.id)
            if ftpquotalimits.quota_type != self.quota_type:
                signals.modify_ftpquotalimits_quotatype_done.send(sender=Ftpquotalimits, obj=self)



        self.username = self.username_id.username
        super(Ftpquotalimits, self).save(*args, **kwargs)
        if first_create == 1:
            signals.create_ftpquotalimits_done.send(sender=Ftpquotalimits, obj=self)







