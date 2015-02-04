from django.conf.urls import patterns, url, include


urlpatterns = patterns('proftpd.ftpadmin.views',
    url(r'^$', 'ftpsetting.define_interface', name="ftpsetting_default"),
    url(r'^ftpsetting/database/$', 'ftpsetting.define_database', name="ftpsetting_define_database"),
    url(r'^ftpsetting/proftpd/$', 'ftpsetting.define_proftpd', name="ftpsetting_define_proftpd"),
    url(r'^ftpsetting/filepath/$', 'ftpsetting.define_filepath', name="ftpsetting_define_filepath"),
    url(r'^ftpsetting/interface/$', 'ftpsetting.define_interface', name="ftpsetting_define_interface"),
    url(r'^.*$', 'ftpusers.user_list', name="ftpuser_inval"),
)
