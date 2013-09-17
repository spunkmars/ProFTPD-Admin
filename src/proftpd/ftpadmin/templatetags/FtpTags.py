#coding=utf-8
from django import template
from proftpd.ftpadmin.lib.common import initlog
from django.core.urlresolvers import reverse

from django.shortcuts import render_to_response, get_object_or_404

from proftpd.ftpadmin.models.ftpusers import Ftpuser

from proftpd.ftpadmin.models.ftpgroups import  Ftpgroup


#logger2 = initlog()
register = template.Library()

def do_get_sort_by_url(parser, token):

    try:  
        tag_name, current_sort_by, target_sort_by = token.split_contents()  
    except:  
        raise template.TemplateSyntaxError, "%r tags error" % token.split_contents[0]

    #另一种取得模板变量值方法 步骤1
    #current_sort_by = parser.compile_filter(current_sort_by)
    #target_sort_by = parser.compile_filter(target_sort_by)

    #logger2.info("hhh%shhh, vvv%svvv,  ddd%sddd" % (tag_name, current_sort_by, target_sort_by) )


    return FtpXferNode(current_sort_by, target_sort_by)



class FtpXferNode(template.Node):

    def __init__(self, current_sort_by, target_sort_by):
        #另一种取得模板变量值方法 步骤2
        #self.current_sort_by = current_sort_by
        #self.target_sort_by = target_sort_by
        self.current_sort_by = template.Variable(current_sort_by)
        self.target_sort_by = template.Variable(target_sort_by)

    def render(self, context):
        
        #另一种取得模板变量值方法 步骤3
        #sort_by = self.current_sort_by.resolve(context, True)
        #target_sort_by = self.target_sort_by.resolve(context, True)

        sort_by = self.current_sort_by.resolve(context)
        target_sort_by = self.target_sort_by.resolve(context)
        if  (sort_by == target_sort_by):
            output_sort_by = '-' + target_sort_by
        else:
            output_sort_by = target_sort_by

        return output_sort_by


register.tag('get_sort_by_url', do_get_sort_by_url)

#----------------------------------------------------------------------------
def do_get_user_url_by_username(parser, token):

    try:  
        tag_name, do_action, user_name = token.split_contents()  
    except:  
        raise template.TemplateSyntaxError, "%r tags error" % token.split_contents[0]
    return FtpUserNode1(do_action, user_name)


class FtpUserNode1(template.Node):
    def __init__(self, do_action, user_name):
        self.user_name = template.Variable(user_name)
        self.do_action = template.Variable(do_action)


    def render(self, context):
        user_name = self.user_name.resolve(context)
        do_action = self.do_action.resolve(context)

        user_detail_url = ''
        url_type = 'ftpuser_user_detail'

        if do_action == 'edit' :
            url_type = 'ftpuser_edit_user'
        elif do_action == 'del' :
            url_type = 'ftpuser_del_user'
        elif do_action == 'detail' :
            url_type = 'ftpuser_user_detail'

        ftpuser = get_object_or_404(Ftpuser, username=user_name)
        if ftpuser :
            user_detail_url = reverse(url_type, args=[ftpuser.id])
        return user_detail_url


register.tag('get_user_url_by_username', do_get_user_url_by_username)


#----------------------------------------------------------------------------
def do_get_user_group_url_by_username(parser, token):

    try:  
        tag_name, user_name = token.split_contents()  
    except:  
        raise template.TemplateSyntaxError, "%r tags error" % token.split_contents[0]
    return FtpUserGroupNode1(user_name)


class FtpUserGroupNode1(template.Node):
    def __init__(self,user_name):
        self.user_name = template.Variable(user_name)


    def render(self, context):
        user_name = self.user_name.resolve(context)

        group_edit_url = ''
        ftpuser = get_object_or_404(Ftpuser, username=user_name)
        if ftpuser :
            ftpgroup = get_object_or_404(Ftpgroup, pk=ftpuser.id)
            if ftpgroup :
                group_edit_url = reverse('ftpgroup_edit_group', args=[ftpgroup.id])
        return group_edit_url


register.tag('get_user_group_url_by_username', do_get_user_group_url_by_username)


def do_get_user_group_url_by_groupname(parser, token):

    try:  
        tag_name, do_action, group_name = token.split_contents()  
    except:  
        raise template.TemplateSyntaxError, "%r tags error" % token.split_contents[0]
    return FtpUserGroupNode2(do_action, group_name)


class FtpUserGroupNode2(template.Node):
    def __init__(self, do_action, group_name):
        self.group_name = template.Variable(group_name)
        self.do_action = template.Variable(do_action)

    def render(self, context):
        group_name = self.group_name.resolve(context)
        do_action = self.do_action.resolve(context)

        group_edit_url = ''
        url_type = 'ftpgroup_group_detail'

        if do_action == 'edit' :
            url_type = 'ftpgroup_edit_group'
        elif do_action == 'del' :
            url_type = 'ftpgroup_del_group'
        elif do_action == 'detail' :
            url_type = 'ftpgroup_group_detail'

        ftpgroup = get_object_or_404(Ftpgroup, groupname=group_name)
        if ftpgroup :
            group_edit_url = reverse(url_type, args=[ftpgroup.id])
        return group_edit_url


register.tag('get_user_group_url_by_groupname', do_get_user_group_url_by_groupname)


#----------------------------------------------------------------------------
def do_get_group_member_html_context(parser, token):

    try:  
        tag_name, mem_str = token.split_contents()  
    except:  
        raise template.TemplateSyntaxError, "%r tags error" % token.split_contents[0]
    return FtpUserGroupNode3(mem_str)


class FtpUserGroupNode3(template.Node):
    def __init__(self, mem_str):
        self.mem_str = template.Variable(mem_str)


    def render(self, context):
        mem_str = self.mem_str.resolve(context)
        mem_html_context = ''
        url_array = []
        mem_array = []
        if mem_str :
            mem_array = mem_str.split(',')
        list_url = reverse('ftpuser_list_user')
        for member in mem_array :
            search_url = list_url + '?q=' + member
            url_array.append('<a href="' + search_url + '">' + member + '</a>')
        mem_html_context = ',&nbsp;'.join(url_array)

        return mem_html_context


register.tag('get_group_member_html_context', do_get_group_member_html_context)