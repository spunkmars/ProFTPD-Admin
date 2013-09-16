
from django.conf.urls.defaults import  *



urlpatterns = patterns('proftpd.ftpadmin.views',
    url(r'^$', 'ftpctrl.session', name="ftpctrl_default"),
    url(r'^session/$', 'ftpctrl.session', name="ftpctrl_session"),
    url(r'^status/$', 'ftpctrl.ftp_status', name="ftpctrl_status"),
    url(r'^.*$', 'ftpusers.user_list', name="ftpctrl_inval"),


)
