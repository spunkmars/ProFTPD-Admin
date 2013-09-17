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
from proftpd.ftpadmin.forms.ftpusers import UserForm
from proftpd.ftpadmin.models.ftpusers import Ftpuser
from proftpd.ftpadmin.models.ftpgroups import  Ftpgroup
from proftpd.ftpadmin.lib.common import initlog



logger2 = initlog()

#class UserForm(ModelForm):
#    #det_notes=forms.CharField(label=u'NOTES', widget=forms.TextInput(attrs={'size':'40'}))
#    #passwd=forms.CharField(label=u'PASSWORD', widget=forms.PasswordInput())
#    class Meta:
#        model = Ftpuser
#        #fields = ('username', 'passwd', 'group')
#        widgets = {
#
#        }
#
#class EditUserForm(ModelForm):
#    #det_notes=forms.CharField(label=u'NOTES', widget=forms.TextInput(attrs={'size':'40'}))
#    #passwd=forms.CharField(label=u'PASSWORD', widget=forms.PasswordInput())
#    class Meta:
#        model = Ftpuser
#        #fields = ('username', 'passwd', 'group')
#        widgets = {
#
#        }



#
#@login_required(redirect_field_name='')
#def user_list(request):
#    return render_to_response('ftpadmin/user_list.html',
#                               { 'user_list': Ftpuser.objects.all()} ,context_instance=RequestContext(request) )




@login_required(redirect_field_name='')
def add_user(request):
    if request.method == 'POST':
        form = UserForm(model=Ftpuser, data=request.POST)
        logger2.info(request)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse('ftpuser_list_user'))
    else:
        form = UserForm(model=Ftpuser
        )

    return render_to_response('ftpadmin/add_user.html', {'form': form} ,context_instance=RequestContext(request))


@login_required(redirect_field_name='')
def edit_user(request, user_id):
    user = get_object_or_404(Ftpuser, pk=user_id)
    if request.method == 'POST':
        form = UserForm(model=Ftpuser, instance=user, data=request.POST)
        if form.is_valid():
           new_user = form.save()
           return HttpResponseRedirect(reverse('ftpuser_list_user'))
    else:
        form = UserForm(model=Ftpuser, instance=user)
    return render_to_response('ftpadmin/edit_user.html',
                                  { 'form': form} ,context_instance=RequestContext(request))


@login_required(redirect_field_name='')
def multiple_done(request):
    invalid_fields = []
    return view_multiple_done(request=request, d_model=Ftpuser, default_url=HttpResponseRedirect(reverse('ftpuser_list_user')), invalid_fields=invalid_fields )



@login_required(redirect_field_name='')
def user_list(request):
    model_object = Ftpuser
    each_page_items = int( SITE_INTERFACE.get('show_ftpuser_items_each_page', 3))
    filter_field = 'username'
    page_nav_base_url = reverse('ftpuser_list_user')
    show_error_url =  reverse('ftpuser_list_user')
    show_list_uri = [{'name':'detail', 'url':'/user/detail', 'title':'detail', 'target':'_self'}, {'name':'edit', 'url':'/user/edit', 'title':'edit', 'target':'_self'}, {'name':'del', 'url':'/user/del', 'title':'del', 'target':'_self'}]
    nav_uri = [{'name':_('Add New User'), 'url':reverse('ftpuser_add_user'), 'title':'add', 'target':'_self'}]
    template_file = 'ftpadmin/user_list.html'
    show_field_list = ['username', 'homedir', 'group', 'count', 'lastlogin', 'expiration', 'disabled']
    render_context = show_items(request=request, mult_action_url=reverse('ftpuser_multiple_done'), show_list_uri = show_list_uri, nav_uri = nav_uri, show_error_url = show_error_url, page_nav_base_url=page_nav_base_url,  model_object=model_object, each_page_items = each_page_items, filter_field = filter_field, template_file = template_file, show_field_list = show_field_list)
    return render_context


@login_required(redirect_field_name='')
def user_detail(request, user_id):
    model_object = Ftpuser
    ftpuser = get_object_or_404(model_object, pk=int(user_id))
    return render_to_response('ftpadmin/user_detail.html',
                                  { 'ftpuser': ftpuser} ,context_instance=RequestContext(request))


@login_required(redirect_field_name='')
def del_user(request, user_id):

    if request.method == "GET":

        confirm_result = request.GET.get('confirm_result', None)
        jump_url = request.GET.get('s_url', reverse('ftpuser_list_user'))
        http_referer = request.META.get('HTTP_REFERER', None)
        if confirm_result != "yes":
            return_result = display_confirm_msg(request=request, http_referer=http_referer, confirm_back_url=http_referer or reverse('ftpuser_list_user'), confirm_msg="You are trying to delete a user , Are you sure to delete it ?", confirm_title='Delete User' )
            return return_result
        elif confirm_result == "yes" :
            del_model_items(del_model=Ftpuser, del_items=user_id)

        return HttpResponseRedirect(jump_url)


@login_required(redirect_field_name='')
def jqplot(request):
    return render_to_response('ftpadmin/jqplot.html')





