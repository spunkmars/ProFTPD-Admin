from django.conf.urls import patterns, url, include


urlpatterns = patterns('proftpd.ftpadmin.views',
    url(r'^$', 'ftpstatus.ftpquotatallies_list_quota', name="ftpstatus_default"),
    url(r'^quotatallies/list/$', 'ftpstatus.ftpquotatallies_list_quota', name="ftpquotatallies_list_quota"),
    url(r'^multiple_done/$', 'ftpstatus.multiple_done', name="ftpquotatallies_multiple_done"),
    url(r'^ftpxferstat/list/$', 'ftpstatus.ftpxferstat_list', name="ftpxferstat_list"),
    url(r'^ftpxferstat/del_transfer_log/$', 'ftpstatus.del_transfer_log', name="del_transfer_log"),
    url(r'^top/$', 'ftpstatus.ftp_top', name="ftp_top"),
    url(r'get_server_info/$', 'ftpstatus.get_server_info', name="get_server_info"),
    url(r'^ajax/$', 'ftpstatus.ajax', name="ajax"),
    url(r'^.*$', 'ftpusers.user_list', name="ftpuser_inval"),
)
