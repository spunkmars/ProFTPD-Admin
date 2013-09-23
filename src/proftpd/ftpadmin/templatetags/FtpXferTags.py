#coding=utf-8
from django import template
from proftpd.ftpadmin.lib.common import initlog

logger2 = initlog()
register = template.Library()

def do_get_field_context(parser, token):

    try:  
        tag_name, field_context_dic, field_name = token.split_contents()  
    except:  
        raise template.TemplateSyntaxError, "%r tags error" % token.split_contents[0]

 


    return FieldContextNode(field_context_dic, field_name)



class FieldContextNode(template.Node):

    def __init__(self, field_context_dic, field_name):

        self.field_context_dic = template.Variable(field_context_dic)
        self.field_name = template.Variable(field_name)

    def render(self, context):

        field_context_dic = self.field_context_dic.resolve(context)
        field_name = self.field_name.resolve(context)
        logger2.info("vvv%svvv,  ddd%sddd" % (str(field_context_dic), field_name) )
        
        #output_field = field_context_dic[field_name]
        output_field = 'hello'
        return output_field

register.tag('get_field_context', do_get_field_context)
