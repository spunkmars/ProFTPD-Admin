#coding=utf-8
import os.path, re
from configobj import ConfigObj
from django.utils.translation import ugettext_lazy as _

from proftpd.settings import PROJECT_PATH
from proftpd.ftpadmin.lib.common import fix_path

PROJECT_PATH = fix_path(PROJECT_PATH)

APP_PATH = os.path.dirname(__file__).replace('\\','/')

#替换路径 "/data/htdocs/www/proftpd/../proftpd/ftpadmin/"中的 'proftpd/../proftpd' 为 'proftpd'.
APP_PATH = fix_path(APP_PATH)




APP_MEDIA =  os.path.join(APP_PATH, 'media').replace('\\','/')

APP_IMAGES =  os.path.join(APP_MEDIA, 'images').replace('\\','/')

APP_UPLOAD = os.path.join(APP_IMAGES, 'upload').replace('\\','/')

APP_STATIC =  os.path.join(APP_PATH, 'static').replace('\\','/')

APP_LIB = os.path.join(APP_PATH, 'lib').replace('\\','/')

APP_CONF = os.path.join(APP_PATH, 'conf').replace('\\','/')

APP_CONF_FILE = os.path.join(APP_CONF, 'ftpadmin.conf').replace('\\','/')

configuration = ConfigObj(APP_CONF_FILE)

LIMIT_DEFAULT_VALUE = configuration['LIMIT_DEFAULT_VALUE']

SITE_INTERFACE = configuration['SITE_INTERFACE']

DATABASE_SERVER =  configuration['DATABASE_SERVER']

FILE_PATH = configuration['FILE_PATH']

#设定user允许的家目录范围
FTP_USER_SAFE_HOMEDIR = ('/data/vhost', '/data/htdocs/www')

#设定gid取值范围
FTP_GROUP_SAFE_GID = (500, 4000)

#设定默认的gid。如果此值为小于0 则不启用，大于0 为启用， 此时任何用户的uid，gid都会固定为此设置值。
FTP_GROUP_DEFAULT_GID = -1

SHELL_CHOICES = (
                 ('/bin/bash', '/bin/bash'),
                 ('/bin/sh', '/bin/sh'),
                 ('/sbin/nologin', '/sbin/nologin'),
                 ('/bin/tcsh', '/bin/tcshell'),
                 ('/bin/csh', '/bin/csh'),
                 ('/bin/ksh', '/bin/ksh'),
)


DISABLED_CHOICES = (
                     (0,  _('False')),
                     (1,  _('True')),
)


#QUOTA_CHOICES = (
#                 ('user', 'user'),
#                 ('group', 'group'),
#                 ('class', 'class'),
#                 ('all', 'all'),
#)

#暂时只支持user限额，其它类型限额将在后续版本添加！
QUOTA_CHOICES = (
                 ('user', 'user'),
)



SESSION_CHOICES = (
                    ('false', _('false')),
                    ('true',  _('true')),
)



LIMIT_CHOICES = (
                  ('hard', 'hard'),
                  ('soft', 'soft'),
 )



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

FTP_ACL_CHOICES = (
                 ('allow', 'allow'),
                 ('deny', 'deny'),
)