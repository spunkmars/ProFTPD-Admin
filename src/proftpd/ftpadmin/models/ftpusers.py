#coding=utf-8
from django.db import models
from proftpd.ftpadmin.models.ftpgroups import Ftpgroup
from proftpd.ftpadmin.lib.common import set_hexdigest, fix_path, check_safe_range, initlog
from proftpd.ftpadmin import signals
from proftpd.ftpadmin.settings import  DISABLED_CHOICES, SHELL_CHOICES, FILE_PATH, FTP_GROUP_DEFAULT_GID, FTP_USER_SAFE_HOMEDIR

logger2 = initlog()

class Ftpuser(models.Model):
    username = models.CharField(max_length=255, unique=True)
    passwd = models.CharField(max_length=255)
    homedir = models.CharField(max_length=255, default=FILE_PATH.get('proftpd_default_data_path', ''))
    shell = models.CharField(max_length=100, choices=SHELL_CHOICES, default="/bin/bash")
    uid = models.IntegerField(editable=False)
    gid = models.IntegerField(editable=False)
    group = models.ForeignKey(Ftpgroup)
    count = models.IntegerField(editable=False, default=0, blank=True, null=True)
    lastlogin = models.DateTimeField(editable=False,  blank=True, null=True)
    lastlogout = models.DateTimeField(editable=False,  blank=True, null=True)
    expiration = models.DateTimeField(blank=True, null=True)
    disabled = models.IntegerField(choices=DISABLED_CHOICES, default='0')
    det_name = models.CharField(blank=True, null=True, max_length=255)
    det_mail = models.EmailField(blank=True, null=True)
    det_address = models.CharField(blank=True, null=True, max_length=255)
    det_notes = models.CharField(blank=True, null=True, max_length=255)

    class Meta:
        db_table = 'ftpusers'
        ordering = ['-username']
        app_label = 'ftpadmin'

    def __unicode__(self):
        return self.username

    #为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in Ftpuser._meta.fields]

    def sync_gid_uid(self):
        if FTP_GROUP_DEFAULT_GID > 0:
            self.uid = int(FTP_GROUP_DEFAULT_GID)
            self.gid = int(FTP_GROUP_DEFAULT_GID)
        else:
            self.uid = self.group.gid
            self.gid = self.group.gid


    def delete(self, *args, **kwargs):
        #del member from group before del user
        self.group.del_group_member(self.username)
        signals.delete_ftpuser_done.send(sender=Ftpuser, obj=self)
        super(Ftpuser, self).delete(*args, **kwargs)


    def save(self, *args, **kwargs):

        if self.id is not None :
            ftpuser = Ftpuser.objects.get(pk=self.id)
            if  ftpuser.passwd != self.passwd :
                self.passwd = set_hexdigest('passwd', self.passwd)

            if ftpuser.group != self.group and ftpuser.username == self.username:
#                self.group = self.group
                self.sync_gid_uid()
                # Del   member from old group
                ftpuser.group.del_group_member(ftpuser.username)
                # Apped member to new group
                self.group.add_group_member(ftpuser.username)


            if ftpuser.group != self.group and ftpuser.username != self.username:
                self.sync_gid_uid()
                ftpuser.group.del_group_member(ftpuser.username)
                self.group.add_group_member(self.username)
                signals.modify_ftpuser_username_done.send(sender=Ftpuser, obj=self)


            #If username by modify, del old username from group
            if ftpuser.group == self.group and ftpuser.username != self.username:
                ftpuser.group.del_group_member(ftpuser.username)
                ftpuser.group.add_group_member(self.username)
                signals.modify_ftpuser_username_done.send(sender=Ftpuser, obj=self)

            if  ftpuser.homedir != self.homedir:
                self.homedir = fix_path(self.homedir)

            self.sync_gid_uid()

        else:
            self.passwd = set_hexdigest('passwd', self.passwd)

            self.group = self.group

            self.sync_gid_uid()
            self.homedir = fix_path(self.homedir)
            #Apped new  member to group
            self.group.add_group_member(self.username)
        
        if check_safe_range(safe_range=FTP_USER_SAFE_HOMEDIR, c_type="startswith", v_value=self.homedir) != True:
            raise ValueError("You must type a valid  homedir!")
            return False

        super(Ftpuser, self).save(*args, **kwargs)
