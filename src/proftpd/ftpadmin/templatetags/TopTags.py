#coding=utf-8
import re

from django import template
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string

from proftpd.ftpadmin.lib.common import initlog
from proftpd.ftpadmin.lib.view_common import show_items
from proftpd.ftpadmin.settings import SITE_INTERFACE
from proftpd.ftpadmin.models.ftpusers import Ftpuser
from proftpd.ftpadmin.models.ftpgroups import  Ftpgroup
from proftpd.ftpadmin.models.ftpquotalimits import  Ftpquotalimits
from proftpd.ftpadmin.models.ftpxferstat import  Ftpxferstat
from proftpd.ftpadmin.models.ftpquotatallies import Ftpquotatallies



#logger2 = initlog()


register = template.Library()

def do_get_top_ftp(parser, token):

    try:  
        #tag_name, field_context_dic, field_name = token.split_contents()
        tag_name, top_type, top_total = token.split_contents()  
    except:  
        raise template.TemplateSyntaxError, "%r tags error" % token.split_contents[0]

    #return TopTagNode(field_context_dic, field_name)
    return TopTagNode(top_type, top_total)


class TopTagNode(template.Node):

#    def __init__(self, field_context_dic, field_name):
    def __init__(self, top_type, top_total):
        self.top_type = top_type
        self.top_total = top_total
        #self.field_context_dic = template.Variable(field_context_dic)
        #self.field_name = template.Variable(field_name)

    def render(self, context):

        #field_context_dic = self.field_context_dic.resolve(context)
        #field_name = self.field_name.resolve(context)
        #logger2.info("vvv%svvv,  ddd%sddd" % (str(field_context_dic), field_name) )
        request = {}
        if self.top_type == 'top_downloader':
            custom_get_parameter = {'query':'', 'sort_by':'-bytes_out_used', 'page':1}
            model_object = Ftpquotatallies
            show_field_list = ['username', 'bytes_out_used', 'files_out_used']
        elif self.top_type == 'top_uploader':
            custom_get_parameter = {'query':'', 'sort_by':'-bytes_in_used', 'page':1}
            model_object = Ftpquotatallies
            show_field_list = ['username', 'bytes_in_used', 'files_in_used']
        elif self.top_type == 'top_loginer':
            custom_get_parameter = {'query':'', 'sort_by':'-count', 'page':1}
            model_object = Ftpuser
            show_field_list = ['username', 'count', 'lastlogin', 'lastlogout']
        else:
            return ''

        if int(SITE_INTERFACE['show_toplist_items_each_section'])>0:
            each_page_items = int(SITE_INTERFACE['show_toplist_items_each_section'])
        else:
            each_page_items = self.top_total
        filter_field = 'username'
        page_nav_base_url = reverse('ftpuser_list_user')
        show_error_url =  reverse('ftpuser_list_user')
        show_list_uri = []
        nav_uri = []
        template_file = 'ftpadmin/top_tag.html'
        return_type = 'render_to_string' # 默认是返回render_to_response,  var则返回变量
        render_content = show_items(request=request, return_type = return_type, custom_get_parameter=custom_get_parameter, show_list_uri = show_list_uri, nav_uri = nav_uri, show_error_url = show_error_url, page_nav_base_url=page_nav_base_url,  model_object=model_object, each_page_items = each_page_items, filter_field = filter_field, template_file = template_file, show_field_list = show_field_list)
        return render_content

register.tag('get_top_ftp', do_get_top_ftp)
