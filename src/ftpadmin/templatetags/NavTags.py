#coding=utf-8

from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

#这句是必须滴
register = template.Library()

#这个类是用来处理Tag的Node的，逻辑很简单
class NavTagItem(template.Node):
    def __init__(self, nav_path):
        self.path = reverse(nav_path.strip('"'))
        #self.text = nav_displaytext.strip('"')
        
    def render(self, context):
        cur_path = context['request'].path
        #context['request']是views传入模板中的request对像，可以通过这种方法从上
        #文对象context中取得
        
        current = False
        if self.path == '/':
            current = cur_path == '/'
        else:
            current = cur_path.startswith(self.path)
            
        cur_id = ''
        if current:
            cur_id = ' id="current" '
            
        #return '<li><a %s href="%s">%s</a></li>' % (cur_id, self.path, self.text)
        return '%s' % cur_id

#注册tag，函数基本就是这个样子，不怎么会有变化    
@register.tag
def navtagitem(parser, token):
    try:
        tag_name, nav_path = token.split_contents()
    except ValueError:
        #msg = "%r tag requires exactly two arguments: path and text" % token.split_contents()[0]
        #raise template.TemplateSyntaxError(msg)
        raise template.TemplateSyntaxError, \
                "%r tag requires exactly two arguments: path and label" % \
                token.split_contents()[0] 
                       
    return NavTagItem(nav_path)