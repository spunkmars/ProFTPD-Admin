#coding=utf-8
import re, os, time, random
import sys

if  sys.version_info >= (2, 6, 0):
    import json as json
else:
    import simplejson as json

from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe 

from proftpd.ftpadmin.lib.common import initlog
from proftpd.ftpadmin.lib.model_common import get_model_relate_field, get_model_valid_fields, mult_save

from proftpd.ftpadmin.settings import APP_IMAGES, APP_UPLOAD

logger2 = initlog()

def show_items(**kwargs):
    each_page_items = int( kwargs.get('each_page_items', 10) )
    show_field_list = kwargs.get('show_field_list', [])
    request =  kwargs.get('request', {})
    page_nav_base_url = kwargs.get('page_nav_base_url', '/')
    show_error_url = kwargs.get('show_error_url', '/')
    show_list_uri = kwargs.get('show_list_uri', [])
    nav_uri = kwargs.get('nav_uri', [])
    custom_get_parameter = kwargs.get('custom_get_parameter', {})
    filter_field = kwargs.get('filter_field', 'id')
    template_file = kwargs.get('template_file', '')
    model_object = kwargs.get('model_object', '')
    return_type = kwargs.get('return_type', 'render_to_response')
    mult_action_url = kwargs.get('mult_action_url', '')

    has_show_list_uri_display = False
    has_nav_uri_display  = False
    after_range_num = 5
    bevor_range_num = 4
    page = 1
    sort_by = ''
    url_prefix_base = ''
    url_sort_prefix = ''
    url_prefix = '?page='
    query=''
    
    if  len(show_list_uri) > 0:
        has_show_list_uri_display = True

    if  len(nav_uri) > 0:
        has_nav_uri_display  = True


    if len(custom_get_parameter) < 1 and request.method == 'GET':

        try:
            page = int(request.GET.get("page",1))
            query = request.GET.get('q', '')
            sort_by = request.GET.get('sort_by', '')
            if page < 1:
                page = 1
        except ValueError:
            page = 1

    else:
        query = custom_get_parameter.get('query', [])
        sort_by = custom_get_parameter.get('sort_by', 'id')
        page = custom_get_parameter.get('page', 1)
        if page < 1:
            page = 1


    #检测sort_by是否在允许的字段中。
    if sort_by is  not None and sort_by != '' and  re.sub('^-', '', sort_by) not in  show_field_list:
        return HttpResponseRedirect(show_error_url)


    sorted_by = sort_by
    if  sort_by is not None and sort_by != '':
        url_sort_prefix = '?sort_by='
        url_prefix = "?page=" 
    else:
        sort_by = '-id'
        url_prefix_base = "?sort_by=%s" % sort_by
        url_sort_prefix =  "?sort_by="
        url_prefix = url_prefix_base + "&page="

    if query is None or query == '':
        if sorted_by is None or sorted_by == '':
            url_sort_prefix = '?sort_by='
            url_prefix = '?page='
        else:
            url_sort_prefix = '?sort_by='
            url_prefix = "?sort_by=%s&page=" % sort_by
        info = model_object.objects.order_by(sort_by).all()
    else:
        if sorted_by is None or sorted_by == '':
            url_prefix_base = "?q=%s" % query
            url_sort_prefix = url_prefix_base + '&sort_by='
            url_prefix = url_prefix_base + '&page='
        else:
            url_prefix_base = "?q=%s" % query
            url_sort_prefix = url_prefix_base + '&sort_by='
            url_prefix = url_prefix_base + "&sort_by=%s&page=" % sort_by
        #filter_Q_string = "Q(%s__contains=\"%s\")" % (kwargs['filter_field'], query)
        info = model_object.objects.order_by(sort_by).filter(eval( "Q(%s__contains=\"%s\")" % (filter_field, query) ))

    paginator = Paginator(info, each_page_items)


    try:
        item_list = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
        item_list = paginator.page(1)

    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+bevor_range_num]
    else:
        page_range = paginator.page_range[0:int(page)+bevor_range_num]

    """可以返回三种类型数据： 
       1、 render_to_response 返回一个 Http Response 有http头部（比如Content-Type: xxx xxx)
       2、 render_to_string  只是返回内容的字符串形式，没有http头部（Content-Type: xxx xxx）
       3、 var     则只是返回 内容的变量（比如 locals）
    """
    if return_type == 'render_to_response':
        return render_to_response(template_file, locals())
    elif return_type == 'render_to_string':
        return render_to_string(template_file, locals())
    elif return_type == 'var':
        return locals()






@csrf_exempt
def check_existing(request):    
    #如果调用Django的Field来处理会自动判断
    #常见的操作是用户上传图片后随机给一个名字
    #所以这里也可以直接返回0，即不存在
    return HttpResponse('0')
 
'''
用来处理的上传图片。如果这个函数独立存在的话，它的request.user
是匿名用户，request.session也和当前登录的用户不同。简单的解决
方法是接传入user_id
'''
@csrf_exempt
def upload_image(request, user_id):
    if request.method == 'POST':
        logger2.info('Start upload image...')
        logger2.info("user_id = %s" % user_id)
        logger2.info(request)
        if request.FILES.get('Filedata', None):
            logger2.info("has attr Filedata")
        logger2.info(request.FILES)
        s_file_name = str(request.FILES['Filedata'].name.encode('utf-8'))
        logger2.info("s_file_name = %s" % s_file_name)
        file_ext = s_file_name.split('.')[-1]
        #file_ext = 'jpg'
        logger2.info("file_ext = %s" % file_ext)
        # 随机或者md5加密或者其他方式，让图片名字不重复
        file_name = time.strftime('%Y%m%d%H%M%S')+str(random.random())[2:10]
        logger2.info("file_name = %s" % file_name)
        user_upload_folder = os.path.join(APP_UPLOAD, user_id)
        logger2.info("user_upload_folder = %s" % user_upload_folder)
        if not os.path.exists(user_upload_folder):
            logger2.info("mkdir %s" % user_upload_folder)
            os.makedirs(user_upload_folder)
        #这里是用二进制的方式操作，Django也提供了其他的方法
        file_upload = open( os.path.join(user_upload_folder, file_name+'.'+file_ext), 'w')
        file_upload.write(request.FILES['Filedata'].read())
        file_upload.close()
        return HttpResponse(file_name+'.'+file_ext)
    else:
        return render_to_response('ftpadmin/uploadify.html', context_instance=RequestContext(request))


def get_modify_actions(model=None, invalid_fields=[]):
    modify_actions = []
    valid_fields = {}
    valid_fields = get_model_valid_fields(model=model, invalid_fields=invalid_fields)
    for field in valid_fields:
        action = {}
        action['value'] = field['name']
        action['text'] = "Modify    " + field['name']
        if len(action) >=2:
            modify_actions.append(action)
    return modify_actions


def get_model_html_output( *args, **kwargs):
    model = kwargs.get('model', None)
    invalid_fields=kwargs.get('invalid_fields', [])
    html_output = {}
    valid_fields = {}
    valid_fields = get_model_valid_fields(model=model, invalid_fields=invalid_fields)
    #print("field_name = %s   field_init = %s\n" % (field_name, field_init))
    for field in valid_fields:
        html_output[field['name']] = field['obj'].formfield().widget.render(field['name'], field['init'])
    return html_output


def view_multiple_done(request=None, d_model=None, default_url=None, invalid_fields=[]):
    http_referer = request.META.get('HTTP_REFERER', None)
    if request.method == 'POST':
        form_data = request.POST.copy()# 这里需要用copy方法【GET属性也需同样处理】，使得form_data为mutable状态，否则下面的del将出错。
        form_type = request.POST.get('form_type', None)
        save_args = {}
        if form_data.has_key('csrfmiddlewaretoken'):
            del form_data['csrfmiddlewaretoken']
        if form_type == None:  #在这里判断POST是否来自动作提交页面！
            if form_data['action'] == 'del_items':
                #logger2.info("select_across = %s" % form_data['select_across'])
                if form_data['select_across'] == '0':
                    return HttpResponseRedirect(http_referer)
                confirm_msg = 'You are trying to delete a item , Are you sure to delete it ?'
                confirm_title = 'Delete Mult items'
                confirm_next_url = ''
                confirm_back_title = 'Back'
                confirm_back_url = http_referer
                return render_to_response('ftpadmin/mult_del_confirm.html',
                              { 'form_type':'mult_delete_form', 'mult_ids':form_data['select_across'], 'confirm_msg':confirm_msg, 'confirm_title':confirm_title, 'confirm_next_url':confirm_next_url, 'confirm_back_title':confirm_back_title, 'confirm_back_url':confirm_back_url } ,context_instance=RequestContext(request))

                
            elif form_data['action'] == 'modify_items':
                field_html_output = json.dumps( get_model_html_output(model=d_model, invalid_fields=invalid_fields), ensure_ascii = False ).replace('\\', '\\\\')#这里需要修复！
                modify_actions = []
                modify_actions = get_modify_actions(model=d_model, invalid_fields=invalid_fields)
                #logger2.info(field_html_output)
                return render_to_response('ftpadmin/mult_modify.html', {'mult_ids': form_data['select_across'], 'field_html_output':field_html_output, 'modify_actions':modify_actions } ,context_instance=RequestContext(request))
        elif form_type == 'mult_modify_form':#在这里判断POST是否来自mult_midify页面！
            mult_ids = form_data.get('mult_ids', None)
            save_args = split_valid_POST_data(form_data=form_data)
            
            mult_save(model=d_model, mult_ids=mult_ids, save_args=save_args)
            return default_url
        elif form_type == 'mult_delete_form':#在这里判断POST是否来自mult_delete页面！
            mult_ids = form_data.get('mult_ids', None)
            save_args = split_valid_POST_data(form_data=form_data)
            del_model_items(del_model=d_model, del_items=mult_ids)
            return default_url
    return HttpResponseRedirect(http_referer)


def safe_hash_del(d_hash={}, d_key=None):
    if d_hash.has_key(d_key):
        del d_hash[d_key]
    return  d_hash


def split_valid_POST_data(form_data={}):
    form_data = safe_hash_del(form_data, 'form_type')
    form_data = safe_hash_del(form_data, 'mult_ids')  
    form_data = safe_hash_del(form_data, 'select_one')
    save_args = {}
    for key in form_data.keys():
        save_args[key] = form_data[key]
    return save_args

def del_model_items( *args, **kwargs ):
    del_model = kwargs.get('del_model', None)
    del_items = kwargs.get('del_items', None)
    if del_items.find(',') != -1:
        mult_ids = []
        mult_ids = del_items.split(',')
        if mult_ids[0] == 'undefined':
            return False
        for p_id in mult_ids:
            del_model_instance = get_object_or_404(del_model, pk=p_id)
            if del_model_instance:
                del_model_instance.delete()
    else:
        del_model_instance = get_object_or_404(del_model, pk=del_items)
        if del_model_instance:
            del_model_instance.delete()


def display_confirm_msg( *args, **kwargs ):

    request = kwargs.get('request', None)
    http_referer = kwargs.get('http_referer', None)
    confirm_back_url = kwargs.get('confirm_back_url', http_referer) 
    confirm_msg = kwargs.get('confirm_msg', None)
    confirm_title = kwargs.get('confirm_title', None)
    confirm_next_url = kwargs.get('confirm_next_url', "%s?confirm_result=yes&s_url=%s" % (request.path, http_referer) )
    confirm_back_title = kwargs.get('confirm_back_title','Back')
    #logger2.info( "%s, %s, %s, %s, %s, %s" % (http_referer, confirm_back_url, confirm_msg, confirm_title, confirm_next_url, confirm_back_title) )
    return render_to_response('ftpadmin/confirm_action.html',
                              { 'confirm_msg':confirm_msg, 'confirm_title':confirm_title, 'confirm_next_url':confirm_next_url, 'confirm_back_title':confirm_back_title, 'confirm_back_url':confirm_back_url } ,context_instance=RequestContext(request))

