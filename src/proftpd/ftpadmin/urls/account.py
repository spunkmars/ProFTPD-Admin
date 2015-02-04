from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^$', 'proftpd.ftpadmin.views.account.login', name='account_default'),
    url(r'^login/$', 'proftpd.ftpadmin.views.account.login', name='account_login'),
    url(r'^logout/$', 'proftpd.ftpadmin.views.account.logout', name='account_logout'),
    url(r'^get_check_code_image/$', 'proftpd.ftpadmin.views.account.get_check_code_image', name='account_get_checkcode_image'),
    url(r'^signup/$', 'proftpd.ftpadmin.views.account.signup', name='account_signup'),
    url(r'^upload_image/(?P<user_id>\d+)/$', 'proftpd.ftpadmin.lib.view_common.upload_image', name='upload_image'),
    url(r'^check_existing/$', 'proftpd.ftpadmin.lib.view_common.check_existing', name='check_existing'),
    url(r'^uploadify/$', 'proftpd.ftpadmin.views.account.uploadify', name='uploadify'),
    url(r'^.*$', 'proftpd.ftpadmin.views.account.login'),

)
