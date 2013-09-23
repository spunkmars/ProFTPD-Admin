from django.conf.urls.defaults import  *


urlpatterns = patterns('proftpd.ftpadmin.views',
    url(r'^$', 'ftpquotalimits.quota_list', name="ftpquotalimit_default"),
    url(r'^add/$', 'ftpquotalimits.add_quota', name="ftpquotalimit_add_quota"),
    url(r'^edit/(?P<quota_id>\d+)/$', 'ftpquotalimits.edit_quota', name="ftpquotalimit_edit_quota"),
    url(r'^del/(?P<quota_id>\d+)/$', 'ftpquotalimits.del_quota', name="ftpquotalimit_del_quota"),
    url(r'^list/$', 'ftpquotalimits.quota_list', name="ftpquotalimit_list_quota"),
    url(r'^multiple_done/$', 'ftpquotalimits.multiple_done', name="ftpquotalimit_multiple_done"),
    url(r'^.*$', 'ftpquotalimits.quota_list', name="ftpquotalimit_inval"),


)