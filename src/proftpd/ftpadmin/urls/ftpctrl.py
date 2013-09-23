
from django.conf.urls.defaults import  *



urlpatterns = patterns('proftpd.ftpadmin.views',
    url(r'^$', 'ftpctrl.session', name="ftpctrl_default"),
    url(r'^session/$', 'ftpctrl.session', name="ftpctrl_session"),
    url(r'^status/$', 'ftpctrl.ftp_status', name="ftpctrl_status"),
    url(r'^control/$', 'ftpctrl.ftp_ctrl', name="ftpctrl_ctrl"),
    url(r'^.*$', 'ftpusers.user_list', name="ftpctrl_inval"),


)
