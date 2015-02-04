from django.conf.urls import patterns, url, include


urlpatterns = patterns('proftpd.ftpadmin.views',
    url(r'^$', 'ftpgroups.group_list', name="ftpgroup_default"),
    url(r'^list/$', 'ftpgroups.group_list', name="ftpgroup_list_group"),
    url(r'^add/$', 'ftpgroups.add_group', name="ftpgroup_add_group"),
    url(r'^edit/(?P<group_id>\d+)/$', 'ftpgroups.edit_group', name="ftpgroup_edit_group"),
    url(r'^detail/(?P<group_id>\d+)/$', 'ftpgroups.group_detail', name="ftpgroup_group_detail"),
    url(r'^del/(?P<group_id>\d+)/$', 'ftpgroups.del_group', name="ftpgroup_del_group"),
    url(r'^multiple_done/$', 'ftpgroups.multiple_done', name="ftpgroup_multiple_done"),
    url(r'^.*$', 'ftpgroups.group_list', name="ftpgroup_inval"),


)
