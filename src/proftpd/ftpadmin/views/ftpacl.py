#coding=utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.urlresolvers import reverse
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _


from proftpd.ftpadmin.lib.view_common import show_items, view_multiple_done, display_confirm_msg
from proftpd.ftpadmin.settings import SITE_INTERFACE
from proftpd.ftpadmin.forms.ftpacl import AclForm
from proftpd.ftpadmin.models.ftpacl import Ftpacl

from proftpd.ftpadmin.lib.common import initlog



logger2 = initlog()



@login_required(redirect_field_name='')
def add_acl(request):
    if request.method == 'POST':
        form = AclForm(model=Ftpacl, data=request.POST)
        if form.is_valid():
            new_acl = form.save()
            return HttpResponseRedirect(reverse('ftpacl_list_acl'))
    else:
        form = AclForm(model=Ftpacl
        )

    return render_to_response('ftpadmin/add_acl.html', {'form': form} ,context_instance=RequestContext(request))


@login_required(redirect_field_name='')
def edit_acl(request, acl_id):
    acl = get_object_or_404(Ftpacl, pk=acl_id)
    if request.method == 'POST':
        form = AclForm(model=Ftpacl, instance=acl, data=request.POST)
        if form.is_valid():
           new_acl = form.save()
           return HttpResponseRedirect(reverse('ftpacl_list_acl'))
    else:
        form = AclForm(model=Ftpacl, instance=acl)
    return render_to_response('ftpadmin/edit_acl.html',
                                  { 'form': form} ,context_instance=RequestContext(request))



@login_required(redirect_field_name='')
def multiple_done(request):
    invalid_fields = ['username_id', 'groupname_id', 'path']
    return view_multiple_done(request=request, d_model=Ftpacl, default_url=HttpResponseRedirect(reverse('ftpacl_list_acl')), invalid_fields=invalid_fields)


@login_required(redirect_field_name='')
def acl_list(request):
    model_object = Ftpacl
    each_page_items = int( SITE_INTERFACE.get('show_ftpacl_items_each_page', 3))
    filter_field = 'path'
    page_nav_base_url = reverse('ftpacl_list_acl')
    show_error_url =  reverse('ftpacl_list_acl')
    show_list_uri = [{'name':'edit', 'url':'/acl/edit', 'title':'edit', 'target':'_self'}, {'name':'del', 'url':'/acl/del', 'title':'del', 'target':'_self'}]
    nav_uri = [{'name':_('Add New ACL'), 'url':reverse('ftpacl_add_acl'), 'title':'add', 'target':'_self'}]
    template_file = 'ftpadmin/acl_list.html'
    show_field_list = ['id', 'username', 'groupname', 'path', 'read_acl', 'write_acl', 'delete_acl', 'create_acl', 'modify_acl', 'move_acl', 'view_acl', 'navigate_acl']
    render_context = show_items(request=request, mult_action_url=reverse('ftpacl_multiple_done'), show_list_uri = show_list_uri, nav_uri = nav_uri, show_error_url = show_error_url, page_nav_base_url=page_nav_base_url,  model_object=model_object, each_page_items = each_page_items, filter_field = filter_field, template_file = template_file, show_field_list = show_field_list)
    return render_context



@login_required(redirect_field_name='')
def acl_detail(request, acl_id):
    model_object = Ftpacl
    ftpacl = get_object_or_404(model_object, pk=int(acl_id))
    return render_to_response('ftpadmin/acl_detail.html',
                                  { 'ftpacl': ftpacl} ,context_instance=RequestContext(request))



 
@login_required(redirect_field_name='')
def del_acl(request, acl_id):

    if request.method == "GET":

        confirm_result = request.GET.get('confirm_result', None)
        jump_url = request.GET.get('s_url', reverse('ftpacl_list_acl'))
        http_referer = request.META.get('HTTP_REFERER', None)
        if confirm_result != "yes":
            
            confirm_back_url = http_referer or reverse('ftpacl_list_acl')
            confirm_msg = "You are trying to delete a acl , Are you sure to delete it ?"
            confirm_title = 'Delete acl'
            confirm_next_url = "%s?confirm_result=yes&s_url=%s" % (request.path, http_referer)
            confirm_back_title = 'Back'
            
    
            return render_to_response('ftpadmin/confirm_action.html',
                                      { 'confirm_msg':confirm_msg, 'confirm_title':confirm_title, 'confirm_next_url':confirm_next_url, 'confirm_back_title':confirm_back_title, 'confirm_back_url':confirm_back_url } ,context_instance=RequestContext(request))
        elif confirm_result == "yes" :
            ftpacl = get_object_or_404(Ftpacl, pk=acl_id)
            if ftpacl:
                ftpacl.delete()

        return HttpResponseRedirect(jump_url)


    
