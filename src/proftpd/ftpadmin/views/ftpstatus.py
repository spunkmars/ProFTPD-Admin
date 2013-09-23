#coding=utf-8
import re

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django import forms
from django.forms import ModelForm
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson 
from django.views.decorators.csrf import csrf_exempt

from proftpd.ftpadmin.settings import SITE_INTERFACE
from proftpd.ftpadmin.lib.common import initlog
from proftpd.ftpadmin.lib.view_common import show_items, view_multiple_done, display_confirm_msg
from proftpd.ftpadmin.lib.ftp_info import proftpd_info
from proftpd.ftpadmin.models.ftpquotalimits import  Ftpquotalimits
from proftpd.ftpadmin.models.ftpxferstat import  Ftpxferstat
from proftpd.ftpadmin.models.ftpquotatallies import Ftpquotatallies


#logger2 = initlog()

#def get_request_GET_info():
#    refer_dict = {}
#    http_refer = split_request_GET_string()
#    refer_list = re.split('^?|\&', http_refer)
#    #把列表转换成字典：
#    refer_dict = dict( [ (k, v) for k,v in zip ( refer_list[::2],refer_list[1::2] ) ] )

######################################################################

@login_required(redirect_field_name='')
def show_ftp_info(request):
    infos = proftpd_info()
    ftp_server_info = infos.online_status()
    return render_to_response("ftpadmin/show_ftp_info.html", {'info':ftp_server_info}, context_instance=RequestContext(request))
 

@login_required(redirect_field_name='')
@csrf_exempt #禁用csrf
def get_server_info(request):
    if request.method == "POST":
     
        #import random
        #num = random.randint(1, 100)
        infos = proftpd_info()
        ftp_server_info = infos.online_status()
        #test_id = request.POST.get('test_id', None)
        #msg = str(num)
    else:
        msg = '失败! 成功一半。。。'
    return HttpResponse(simplejson.dumps(ftp_server_info,ensure_ascii = False), mimetype="application/json") 



@login_required(redirect_field_name='')
def ajax(request):
    return render_to_response("ftpadmin/ajax.html", context_instance=RequestContext(request))


@login_required(redirect_field_name='')
def ftpxferstat_list(request):
    model_object = Ftpxferstat
    each_page_items = int( SITE_INTERFACE.get('show_ftpxferstat_items_each_page', 30))
    filter_field = 'username'
    page_nav_base_url = reverse('ftpxferstat_list')
    show_error_url = reverse('ftpxferstat_list')
    show_list_uri = []
    nav_uri = []
    template_file = 'ftpadmin/xferstat_list.html'
    show_field_list = ['id', 'username', 'file', 'size', 'address_full', 'address_ip', 'command', 'timespent', 'time', 'cmd' ]
    #show_field_list = ['id', 'username', 'file']
    render_context = show_items(request=request, show_list_uri = show_list_uri, nav_uri = nav_uri, show_error_url = show_error_url, page_nav_base_url=page_nav_base_url, model_object=model_object, each_page_items = each_page_items, filter_field = filter_field, template_file = template_file, show_field_list = show_field_list)
    return render_context


@login_required(redirect_field_name='')
def ftpquotatallies_list_quota(request):
    model_object = Ftpquotatallies
    each_page_items = int( SITE_INTERFACE.get('show_ftpquota_items_each_page', 3))
    filter_field = 'username'
    page_nav_base_url = reverse('ftpquotatallies_list_quota')
    show_error_url =  reverse('ftpquotatallies_list_quota')
    show_list_uri = []
    nav_uri = []
    template_file = 'ftpadmin/quotatallies_list.html'
    show_field_list = ['id', 'username', 'quota_type', 'bytes_in_used', 'bytes_out_used', 'bytes_xfer_used', 'files_in_used', 'files_out_used', 'files_xfer_used']
    #show_field_list = ['id', 'username', 'file']
    render_context = show_items(request=request, mult_action_url=reverse('ftpquotatallies_multiple_done'), show_list_uri = show_list_uri, nav_uri = nav_uri, show_error_url = show_error_url, page_nav_base_url=page_nav_base_url,  model_object=model_object, each_page_items = each_page_items, filter_field = filter_field, template_file = template_file, show_field_list = show_field_list)
    return render_context

@login_required(redirect_field_name='')
def multiple_done(request):
    invalid_fields = ['username_id']
    return view_multiple_done(request=request, d_model=Ftpquotatallies, default_url=HttpResponseRedirect(reverse('ftpquotatallies_list_quota')), invalid_fields=invalid_fields )


@login_required(redirect_field_name='')
def ftp_top(request):
    return render_to_response("ftpadmin/top.html", context_instance=RequestContext(request))

######################################################################

@login_required(redirect_field_name='')
def  del_transfer_log (request):

    if request.method == 'POST':
        try:
            del_date_0 = request.POST.get("date_0", '')
            del_date_1 = request.POST.get("date_1", '')
            del_date = del_date_0 + ' ' + del_date_1 
            del_username =  request.POST.get("username", '')
        except ValueError:
            del_date = ''
            del_username = ''

        if ( del_date is None or del_date == '' ) and  (del_username is None or del_username == ''):
            return render_to_response("ftpadmin/del_transfer_log.html")
        elif ( del_date is None or del_date == '' ) and  (del_username is not None and del_username != ''):
            #Ftpxferstat.objects.filter(Q(username__contains=del_username)).delete()
            Ftpxferstat.objects.filter(username=del_username).delete()
        elif ( del_date is not None and del_date != '' ) and  (del_username is  None or del_username == ''):
            #Ftpxferstat.objects.filter(Q(time__contains=del_date)).delete()
            Ftpxferstat.objects.filter(time__lt=del_date).delete()
        elif ( del_date is not None and del_date != '' ) and  (del_username is not  None and del_username != ''):
            Ftpxferstat.objects.filter(time__lt=del_date, username=del_username).delete()

        return HttpResponseRedirect(reverse('ftpxferstat_list'))
    else:
        return render_to_response("ftpadmin/del_transfer_log.html", context_instance=RequestContext(request))

