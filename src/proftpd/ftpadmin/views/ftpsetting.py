#coding=utf-8
from configobj import ConfigObj
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

from proftpd.ftpadmin.lib.common import initlog
from proftpd.ftpadmin.settings import  APP_CONF_FILE






@login_required(redirect_field_name='')
def define_proftpd(request):
    

    configuration = ConfigObj(APP_CONF_FILE)

    if request.method == 'POST':
        config_data = {}
        form_data = request.POST
        for form_key in form_data.keys():
          if form_key == 'csrfmiddlewaretoken':
              continue
          config_data[form_key] = form_data.get(form_key, '') 
        configuration_w = ConfigObj()
        configuration_w.filename = APP_CONF_FILE
        configuration_w['LIMIT_DEFAULT_VALUE'] = config_data
        configuration.merge(configuration_w)
        configuration.write()
        #configuration_w.write()
        return HttpResponseRedirect(reverse('ftpsetting_define_proftpd'))

    else:
        return render_to_response("ftpadmin/setting_proftpd.html", locals() )




@login_required(redirect_field_name='')
def define_database(request):
    

    configuration = ConfigObj(APP_CONF_FILE)

    if request.method == 'POST':
        config_data = {}
        form_data = request.POST
        for form_key in form_data.keys():
          if form_key == 'csrfmiddlewaretoken':
              continue
          config_data[form_key] = form_data.get(form_key, '') 
        configuration_w = ConfigObj()
        configuration_w.filename = APP_CONF_FILE
        configuration_w['DATABASE_SERVER'] = config_data
        configuration.merge(configuration_w)
        configuration.write()
        return HttpResponseRedirect(reverse('ftpsetting_define_database'))

    else:
        return render_to_response("ftpadmin/setting_database.html", locals() )



@login_required(redirect_field_name='')
def define_interface(request):
    

    configuration = ConfigObj(APP_CONF_FILE)

    if request.method == 'POST':
        config_data = {}
        form_data = request.POST
        for form_key in form_data.keys():
          if form_key == 'csrfmiddlewaretoken':
              continue
          config_data[form_key] = form_data.get(form_key, '') 
        configuration_w = ConfigObj()
        configuration_w.filename = APP_CONF_FILE
        configuration_w['SITE_INTERFACE'] = config_data
        configuration.merge(configuration_w)
        configuration.write()
        return HttpResponseRedirect(reverse('ftpsetting_define_interface'))

    else:
        return render_to_response("ftpadmin/setting_interface.html",  locals() )



@login_required(redirect_field_name='')
def define_filepath(request):
    

    configuration = ConfigObj(APP_CONF_FILE)

    if request.method == 'POST':
        config_data = {}
        form_data = request.POST
        for form_key in form_data.keys():
          if form_key == 'csrfmiddlewaretoken':
              continue
          config_data[form_key] = form_data.get(form_key, '') 
        configuration_w = ConfigObj()
        configuration_w.filename = APP_CONF_FILE
        configuration_w['FILE_PATH'] = config_data
        configuration.merge(configuration_w)
        configuration.write()
        return HttpResponseRedirect(reverse('ftpsetting_define_filepath'))

    else:
        return render_to_response("ftpadmin/setting_filepath.html",  locals() )
