from django.conf.urls import patterns, url, include


urlpatterns = patterns('proftpd.ftpadmin.views',
    url(r'^$', 'ftpusers.user_list', name="ftpuser_default"),
    url(r'^add/$', 'ftpusers.add_user', name="ftpuser_add_user"),
    url(r'^edit/(?P<user_id>\d+)/$', 'ftpusers.edit_user', name="ftpuser_edit_user"),
    url(r'^detail/(?P<user_id>\d+)/$', 'ftpusers.user_detail', name="ftpuser_user_detail"),
    url(r'^del/(?P<user_id>\d+)/$', 'ftpusers.del_user', name="ftpuser_del_user"),
    url(r'^list/$', 'ftpusers.user_list', name="ftpuser_list_user"),
    url(r'^multiple_done/$', 'ftpusers.multiple_done', name="ftpuser_multiple_done"),
    url(r'^jqplot/$', 'ftpusers.jqplot', name="ftpuser_jqplot"),
    url(r'^.*$', 'ftpusers.user_list', name="ftpuser_inval"),


)
