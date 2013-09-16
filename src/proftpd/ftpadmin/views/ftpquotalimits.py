#coding=utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django import forms
from django.forms import ModelForm
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from proftpd.ftpadmin.lib.view_common import show_items, view_multiple_done, display_confirm_msg
from proftpd.ftpadmin.settings import SITE_INTERFACE
from proftpd.ftpadmin.lib.common import initlog
from proftpd.ftpadmin.forms.ftpquotalimits import QuotaLimitsForm
from proftpd.ftpadmin.models.ftpquotalimits import  Ftpquotalimits

#logger2 = initlog()




@login_required(redirect_field_name='')
def add_quota(request):
    if request.method == 'POST':

        form = QuotaLimitsForm(model=Ftpquotalimits, data=request.POST)
        if form.is_valid():
            new_quota = form.save()
            return HttpResponseRedirect(reverse('ftpquotalimit_list_quota'))
    else:
        form = QuotaLimitsForm(model=Ftpquotalimits)

    return render_to_response('ftpadmin/add_quota.html', {'form': form} ,context_instance=RequestContext(request))




@login_required(redirect_field_name='')
def edit_quota(request, quota_id):
    quota = get_object_or_404(Ftpquotalimits, pk=quota_id)
    if request.method == 'POST':

        form = QuotaLimitsForm(model=Ftpquotalimits, instance=quota, data=request.POST)
        if form.is_valid():
           new_quota = form.save()
           return HttpResponseRedirect(reverse('ftpquotalimit_list_quota'))
    else:
        form = QuotaLimitsForm(model=Ftpquotalimits, instance=quota)

    return render_to_response('ftpadmin/edit_quota.html',
                                  { 'form': form} ,context_instance=RequestContext(request))


@login_required(redirect_field_name='')
def multiple_done(request):
    invalid_fields = ['username_id']
    return view_multiple_done(request=request, d_model=Ftpquotalimits, default_url=HttpResponseRedirect(reverse('ftpquotalimit_list_quota')), invalid_fields=invalid_fields )


@login_required(redirect_field_name='')
def quota_list(request):
    model_object = Ftpquotalimits
    each_page_items = int( SITE_INTERFACE.get('show_ftplimit_items_each_page', 3))
    filter_field = 'username'
    page_nav_base_url = reverse('ftpquotalimit_list_quota')
    show_error_url =  reverse('ftpquotalimit_list_quota')
    show_list_uri = [{'name':'edit', 'url':'/quota/edit', 'title':'edit', 'target':'_self'}, {'name':'del', 'url':'/quota/del', 'title':'del', 'target':'_self'}]
    nav_uri = [{'name':_('Add New Quota'), 'url':reverse('ftpquotalimit_add_quota'), 'title':'add', 'target':'_self'}]
    template_file = 'ftpadmin/quota_list.html'
    show_field_list = ['id', 'username', 'quota_type', 'per_session', 'limit_type', 'bytes_in_avail', 'bytes_out_avail', 'bytes_xfer_avail', 'files_in_avail', 'files_out_avail', 'files_xfer_avail']
    render_context = show_items(request=request, mult_action_url=reverse('ftpquotalimit_multiple_done'), show_list_uri = show_list_uri, nav_uri = nav_uri, show_error_url = show_error_url, page_nav_base_url=page_nav_base_url,  model_object=model_object, each_page_items = each_page_items, filter_field = filter_field, template_file = template_file, show_field_list = show_field_list)
    return render_context




@login_required(redirect_field_name='')
def del_quota(request, quota_id):

    if request.method == "GET":

        confirm_result = request.GET.get('confirm_result', None)
        jump_url = request.GET.get('s_url', reverse('ftpquotalimit_list_quota'))
        http_referer = request.META.get('HTTP_REFERER', None)
        if confirm_result != "yes":
            
            confirm_back_url = http_referer or reverse('ftpquotalimit_list_quota')
            confirm_msg = "You are trying to delete a user quota , Are you sure to delete it ?"
            confirm_title = 'Delete Quota'
            confirm_next_url = "%s?confirm_result=yes&s_url=%s" % (request.path, http_referer)
            confirm_back_title = 'Back'
            
    
            return render_to_response('ftpadmin/confirm_action.html',
                                      { 'confirm_msg':confirm_msg, 'confirm_title':confirm_title, 'confirm_next_url':confirm_next_url, 'confirm_back_title':confirm_back_title, 'confirm_back_url':confirm_back_url } ,context_instance=RequestContext(request))
        elif confirm_result == "yes" :
            ftpquotalimits = get_object_or_404(Ftpquotalimits, pk=quota_id)
            if ftpquotalimits:
                ftpquotalimits.delete()

        return HttpResponseRedirect(jump_url)