#from django.conf.urls.defaults import patterns, include, url
from django.conf.urls import patterns, url, include

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

#handler403 = 'mysite.views.my_custom_permission_denied_view'
#handler404 = 'mysite.views.my_custom_404_view'
#handler500 = 'mysite.views.my_custom_error_view'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'proftpd.views.home', name='home'),
    # url(r'^proftpd/', include('proftpd.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/media/'}),
    url(r'^$', 'proftpd.ftpadmin.views.ftpstatus.show_ftp_info', name="site_index"),
#    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/setlang', 'proftpd.ftpadmin.views.account.set_language', name="set_language"),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^ftpctrl/', include('proftpd.ftpadmin.urls.ftpctrl')),
    url(r'^account/', include('proftpd.ftpadmin.urls.account')),
    url(r'^group/', include('proftpd.ftpadmin.urls.ftpgroups')),
    url(r'^user/', include('proftpd.ftpadmin.urls.ftpusers')),
    url(r'^quota/', include('proftpd.ftpadmin.urls.ftpquota')),
    url(r'^acl/', include('proftpd.ftpadmin.urls.ftpacl')),
    url(r'^status/', include('proftpd.ftpadmin.urls.ftpstatus')),
    url(r'^setting/', include('proftpd.ftpadmin.urls.ftpsetting')),

)
