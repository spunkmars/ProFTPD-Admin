from django import template




register = template.Library()

def do_get_account_status(parser, token):
    return AccountStatusNode()



class AccountStatusNode(template.Node):
    def render(self, context):
        #context['account'] = account.status()
        context['account_status'] = 'test';
        return ''




register.tag('get_account_status', do_get_account_status)