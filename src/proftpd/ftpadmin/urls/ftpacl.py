from django.conf.urls import patterns, url, include


urlpatterns = patterns('proftpd.ftpadmin.views',
    url(r'^$', 'ftpacl.acl_list', name="ftpacl_default"),
    url(r'^list/$', 'ftpacl.acl_list', name="ftpacl_list_acl"),
    url(r'^add/$', 'ftpacl.add_acl', name="ftpacl_add_acl"),
    url(r'^edit/(?P<acl_id>\d+)/$', 'ftpacl.edit_acl', name="ftpacl_edit_acl"),
    url(r'^detail/(?P<acl_id>\d+)/$', 'ftpacl.acl_detail', name="ftpacl_acl_detail"),
    url(r'^del/(?P<acl_id>\d+)/$', 'ftpacl.del_acl', name="ftpacl_del_acl"),
    url(r'^multiple_done/$', 'ftpacl.multiple_done', name="ftpacl_multiple_done"),
    url(r'^.*$', 'ftpacl.acl_list', name="ftpacl_inval"),


)
