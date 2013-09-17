#coding=utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.core.paginator import Paginator,  InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from proftpd.ftpadmin.lib.view_common import show_items, view_multiple_done, display_confirm_msg
from proftpd.ftpadmin.settings import SITE_INTERFACE
from proftpd.ftpadmin.lib.common import initlog
from proftpd.ftpadmin import signals
from proftpd.ftpadmin.forms.ftpgroups import GroupForm
from proftpd.ftpadmin.models.ftpgroups import  Ftpgroup


logger2 = initlog()


# @login_required(redirect_field_name='', login_url='/login/')
@login_required(redirect_field_name='')
def add_group(request):
    if request.method == 'POST':
        #form = GroupForm(request.POST)
        form = GroupForm(model=Ftpgroup, data=request.POST)
        if form.is_valid():
            new_group = form.save()
            return HttpResponseRedirect(reverse('ftpgroup_list_group'))
    else:
        form = GroupForm(model=Ftpgroup)
    is_login = True
    return render_to_response('ftpadmin/add_group.html', {'form': form} ,context_instance=RequestContext(request))


@login_required(redirect_field_name='')
def edit_group(request, group_id):
    group = get_object_or_404(Ftpgroup, pk=group_id)

    if request.method == 'POST':
        #form = EditGroupForm(request.POST)
        form = GroupForm(model=Ftpgroup, instance=group, data=request.POST)
        if form.is_valid():
           new_group = form.save()

           return HttpResponseRedirect(reverse('ftpgroup_list_group'))
    else:
        form = GroupForm(model=Ftpgroup, instance=group)

    return render_to_response('ftpadmin/edit_group.html',
                                  { 'form': form} ,context_instance=RequestContext(request))

@login_required(redirect_field_name='')
def multiple_done(request):
    invalid_fields = []
    return view_multiple_done(request=request, d_model=Ftpgroup, default_url=HttpResponseRedirect(reverse('ftpgroup_list_group')), invalid_fields=invalid_fields )



@login_required(redirect_field_name='')
def group_list(request):
    model_object = Ftpgroup
    each_page_items = int( SITE_INTERFACE.get('show_ftpgroup_items_each_page', 3))
    filter_field = 'groupname'
    page_nav_base_url = reverse('ftpgroup_list_group')
    show_error_url =  reverse('ftpgroup_list_group')
    show_list_uri = [ {'name':'detail', 'url':'/group/detail', 'title':'detail', 'target':'_self'}, {'name':'edit', 'url':'/group/edit', 'title':'edit', 'target':'_self'}, {'name':'del', 'url':'/group/del', 'title':'del', 'target':'_self'}]
    nav_uri = [{'name':'Add New Group', 'url':reverse('ftpgroup_add_group'), 'title':'Add New Group', 'target':'_self'}]
    template_file = 'ftpadmin/group_list.html'
    show_field_list = [ 'groupname', 'gid', 'members', 'expiration' ]
    render_context = show_items(request=request, mult_action_url=reverse('ftpgroup_multiple_done'), show_list_uri = show_list_uri, nav_uri = nav_uri, show_error_url = show_error_url, page_nav_base_url=page_nav_base_url,  model_object=model_object, each_page_items = each_page_items, filter_field = filter_field, template_file = template_file, show_field_list = show_field_list)
    return render_context


@login_required(redirect_field_name='')
def group_detail(request, group_id):
    model_object = Ftpgroup
    ftpgroup = get_object_or_404(model_object, pk=int(group_id))
    return render_to_response('ftpadmin/group_detail.html',
                                  { 'ftpgroup': ftpgroup} ,context_instance=RequestContext(request))


@login_required(redirect_field_name='')
def del_group(request, group_id):

    if request.method == "GET":
        logger2.info(request)
        confirm_result = request.GET.get('confirm_result', None)
        jump_url = request.GET.get('s_url', reverse('ftpgroup_list_group'))
        http_referer = request.META.get('HTTP_REFERER', None)
        if confirm_result != "yes":
            
            confirm_back_url = http_referer or reverse('ftpgroup_list_group')
            confirm_msg = "You are trying to delete a group , Are you sure to delete it ?"
            confirm_title = 'Delete Group'
            confirm_next_url = "%s?confirm_result=yes&s_url=%s" % (request.path, http_referer)
            confirm_back_title = 'Back'
            
    
            return render_to_response('ftpadmin/confirm_action.html',
                                      { 'confirm_msg':confirm_msg, 'confirm_title':confirm_title, 'confirm_next_url':confirm_next_url, 'confirm_back_title':confirm_back_title, 'confirm_back_url':confirm_back_url } ,context_instance=RequestContext(request))
        elif confirm_result == "yes" :
            ftpgroup = get_object_or_404(Ftpgroup, pk=group_id)
            if ftpgroup:
                ftpgroup.delete()

        return HttpResponseRedirect(jump_url)

