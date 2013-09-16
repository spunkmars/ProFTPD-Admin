#coding=utf-8
from django.db import models

from proftpd.ftpadmin.lib.common import set_hexdigest, fix_path, check_safe_range
from proftpd.ftpadmin.settings import  DISABLED_CHOICES, SHELL_CHOICES, FILE_PATH, FTP_GROUP_DEFAULT_GID, FTP_USER_SAFE_HOMEDIR, FTP_ACL_CHOICES
from proftpd.ftpadmin import signals 
from proftpd.ftpadmin.models.ftpgroups import Ftpgroup
from proftpd.ftpadmin.models.ftpusers import Ftpuser


# ACL       Commands     
# READ       RETR 
# WRITE       APPE, STOR, STOU 
# DELETE       DELE, RMD, XRMD 
# CREATE       MKD, XMKD, LINK, SYMLINK 
# MODIFY       MFF, MFMT, SITE CHGRP, SITE CHMOD, SETSTAT, FSETSTAT 
# MOVE       RNFR, RNTO, SITE CPTO, RENAME 
# VIEW       LIST, MDTM, MLSD, MLST, NLST, SIZE, STAT, LSTAT, OPENDIR, READLINK 
# NAVIGATE       CDUP, XCDUP, CWD, XCWD, PWD, XPWD, REALPATH 


#  ACL columns value:
#
#    true/false
#    on/off
#    allow/deny
#    allowed/denied
#    yes/no 


#FTP_ACL_CHOICES = (
#                 ('true', 'true'),
#                 ('false', 'false'),
#                 ('on', 'on'),
#                 ('off', 'off'),
#                 ('allow', 'allow'),
#                 ('deny', 'deny'),
#                 ('allowed', 'allowed'),
#                 ('denied', 'denied'),
#                 ('yes', 'yes'),
#                 ('no', 'no'),
#)

#FTP_ACL_CHOICES = (
#                 ('allow', 'allow'),
#                 ('deny', 'deny'),
#)


class Ftpacl(models.Model):
    username_id = models.IntegerField(null=True, blank=True, unique=False)
    username = models.CharField(max_length=255,  blank=True, null=True,  editable=False)
    groupname_id = models.IntegerField(null=True,  blank=True, unique=False)
    groupname = models.CharField(max_length=255,  blank=True, null=True,  editable=False)
    path = models.CharField(max_length=255, default=FILE_PATH.get('proftpd_default_data_path', ''))
    read_acl = models.CharField(max_length=255, choices=FTP_ACL_CHOICES,  blank=True, null=True, default='allow')
    write_acl = models.CharField(max_length=255, choices=FTP_ACL_CHOICES,  blank=True, null=True, default='deny')
    delete_acl = models.CharField(max_length=255, choices=FTP_ACL_CHOICES,  blank=True, null=True, default='deny')
    create_acl = models.CharField(max_length=255, choices=FTP_ACL_CHOICES,  blank=True, null=True, default='deny')
    modify_acl = models.CharField(max_length=255, choices=FTP_ACL_CHOICES,  blank=True, null=True, default='deny')
    move_acl = models.CharField(max_length=255, choices=FTP_ACL_CHOICES,  blank=True, null=True, default='deny')
    view_acl = models.CharField(max_length=255, choices=FTP_ACL_CHOICES,  blank=True, null=True, default='allow')
    navigate_acl = models.CharField(max_length=255, choices=FTP_ACL_CHOICES,  blank=True, null=True, default='allow')

    class Meta:
        db_table = 'ftpacl'
        ordering = ['-path']
        app_label = 'ftpadmin'

    def __unicode__(self):
        return self.path

    #为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in Ftpacl._meta.fields]

    def sync_username_groupname(self):
        if self.username_id:
            self.username =  Ftpuser.objects.get( pk=int(self.username_id) ).username
        else:
            self.username = ''

        if self.groupname_id:
            self.groupname =  Ftpgroup.objects.get( pk=int(self.groupname_id) ).groupname
        else:
            self.groupname = ''



    def save(self, *args, **kwargs):

        if self.username_id.isdigit():
            self.username_id = int( self.username_id )
        else:
            self.username_id = None

        if self.groupname_id.isdigit():
            self.groupname_id = int( self.groupname_id )
        else:
            self.groupname_id = None

        self.sync_username_groupname()

        if check_safe_range(safe_range=FTP_USER_SAFE_HOMEDIR, c_type="startswith", v_value=self.path) != True:
            raise ValueError("You must type a valid  path!")
            return None
        self.path = fix_path(self.path)

        super(Ftpacl, self).save(*args, **kwargs)