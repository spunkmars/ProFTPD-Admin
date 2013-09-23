#coding=utf-8
import re
from django.db import models
from proftpd.ftpadmin import signals
from proftpd.ftpadmin.lib.common import check_safe_range, initlog
from proftpd.ftpadmin.settings import  DISABLED_CHOICES, FTP_GROUP_SAFE_GID



class Ftpgroup(models.Model):
    groupname = models.CharField(max_length=255, unique=True)
    gid = models.IntegerField()
    members = models.CharField(blank=True, null=True, max_length=255, editable=False)
    expiration = models.DateTimeField(blank=True, null=True)
    disabled = models.IntegerField(choices=DISABLED_CHOICES, default='0')
    description = models.CharField(blank=True, null=True, max_length=255)

    class Meta:
        db_table = 'ftpgroups'
        ordering = ['-groupname']
        app_label = 'ftpadmin'

    def __unicode__(self):
       return self.groupname

    #为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in Ftpgroup._meta.fields]


    def remove_item(self, del_item, lists):
        while lists :
            if del_item in  lists :
                lists.remove(del_item)
            else:
                break
        return lists

    def clean_string(self, aString):
        bString = re.sub('^(\s*,*)+|(\s*,*)+$', '', aString)
        bString = re.sub('(\s*,+\s*)+', ',', bString)
        return bString

    def add_group_member(self, add_member):

#        logger2.info(add_member+'***add')

        if self.members is not None:
            member_list = set( self.members.split(',') )
        else:
            member_list = set()

        if add_member is not None:
            member_list.add(add_member)
        self.members = self.clean_string( ','.join(member_list) )
#        logger2.info(','.join(member_list)+'*2')
        self.save()


    def del_group_member(self, del_member):

#        logger2.info(del_member+'***del')


        if self.members is not None:
            member_list = set( self.members.split(',') )
        else:
            member_list = set()


#        logger2.info(','.join(member_list)+'*3')
        if del_member is not None:
            try:
                member_list.remove(del_member)
            except:
                pass
        self.members = self.clean_string( ','.join(member_list) )
#        logger2.info(','.join(member_list)+'*4')
        self.save()


    def delete(self, *args, **kwargs):

        signals.delete_ftpgroup_done.send(sender=Ftpgroup, obj=self)
        super(Ftpgroup, self).delete(*args, **kwargs)



    def save(self, *args, **kwargs):
        #检测gid是否在允许的范围内！
        if check_safe_range(safe_range=FTP_GROUP_SAFE_GID, c_type="number", v_value=self.gid) != True:
            raise ValueError("You must type a valid  gid !")
            return False

        if self.id is not None:
            ftpgroup = Ftpgroup.objects.get(pk=self.id)

            if ftpgroup.gid != self.gid :
                signals.modify_ftpgroup_gid_done.send(sender=Ftpgroup, obj=self)

            if ftpgroup.groupname != self.groupname :
                signals.modify_ftpgroup_groupname_done.send(sender=Ftpgroup, obj=self)




        super(Ftpgroup, self).save(*args, **kwargs)



