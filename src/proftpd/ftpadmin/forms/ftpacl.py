#coding=utf-8
import datetime
from django import forms
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple, SplitDateTimeWidget
from django.forms.extras.widgets import SelectDateWidget
from django.db.models.fields import BLANK_CHOICE_DASH
from django.utils.translation import ugettext_lazy as _

from proftpd.ftpadmin.lib.form_common import newModelForm, set_select_choice, EXPIRATION_YEAR_CHOICES
from proftpd.ftpadmin.settings import FTP_USER_SAFE_HOMEDIR
from proftpd.ftpadmin.models.ftpgroups import Ftpgroup
from proftpd.ftpadmin.models.ftpusers import Ftpuser
from proftpd.ftpadmin.models.ftpacl import Ftpacl
from proftpd.ftpadmin.lib.common import check_safe_range, check_invalid_path_format, fix_path


class AclForm(newModelForm):

    username_id = forms.ChoiceField(choices=(), required=False, label=_('The Name of user')+' :')
    username = forms.CharField( widget=forms.HiddenInput(), required=False)
    groupname_id = forms.ChoiceField(choices=(), required=False, label=_('The Name of group')+' :')
    groupname = forms.CharField( widget=forms.HiddenInput(), required=False)
    path = forms.CharField(max_length=255, required=True, label=_('Path')+' :')
    read_acl = forms.ChoiceField(choices=(), label=_('Read')+' :')
    write_acl = forms.ChoiceField(choices=(), label=_('Write')+' :')
    delete_acl = forms.ChoiceField(choices=(), label=_('Delete')+' :')
    create_acl = forms.ChoiceField(choices=(), label=_('Create')+' :')
    modify_acl = forms.ChoiceField(choices=(), label=_('Modify')+' :')
    move_acl = forms.ChoiceField(choices=(), label=_('Move')+' :')
    view_acl = forms.ChoiceField(choices=(), label=_('View')+' :')
    navigate_acl = forms.ChoiceField(choices=(), label=_('Navigate')+' :')


    def init_edit_form(self):
        pass


    def init_form_filed_choices(self, field_name=None, s_model=None):
        pk_list = []
        choices = []

        if self.instance:
            if getattr(self.instance, field_name):
                choices = ( (getattr(self.instance, field_name), s_model.objects.get(pk=getattr(self.instance, field_name)).__unicode__()), )
                self.fields[field_name].choices = choices 
            else:
                choices = BLANK_CHOICE_DASH + list(choices)
        else:
            pk_list = [ pk_value[0] for pk_value in s_model.objects.all().values_list('id') ]
            choices = [ (pk_value, s_model.objects.get( pk=pk_value).__unicode__() ) for pk_value in pk_list ]
            choices =  BLANK_CHOICE_DASH + list(choices)
            self.fields[field_name].choices = choices    

    def init_after(self):
        self.init_form_filed_choices(field_name="username_id", s_model=Ftpuser)
        self.init_form_filed_choices(field_name="groupname_id", s_model=Ftpgroup)



    def clean_path(self):
        has_invalid_format = False
        has_unsafe_path = False
        if check_invalid_path_format(self.cleaned_data['path']):
            has_invalid_format = True
            raise forms.ValidationError(_('You must type a valid  path!') + "  Make sure the path not contains a special string (../ or ./ or // or /.) ")
        else:
            has_invalid_format = False

        if len(FTP_USER_SAFE_HOMEDIR):
            safe_homedir_string = '"' + '", "'.join(FTP_USER_SAFE_HOMEDIR) + '"'
            if check_safe_range(safe_range=FTP_USER_SAFE_HOMEDIR, c_type="startswith", v_value=self.cleaned_data['path']) == True:
                has_unsafe_path = False
            else:
                has_unsafe_path = True
                raise forms.ValidationError(_('You must type a valid  path!') + "  for example : %s ." % safe_homedir_string)
        else:
            has_unsafe_path = False

        if has_invalid_format == False and has_unsafe_path == False:
            return  self.cleaned_data['path']

    def has_duplicate_ftpacl_item(self):
        tmp_username = ''
        tmp_groupname = ''
        
        if self.cleaned_data['username_id']:
            tmp_username = Ftpuser.objects.get(pk=self.cleaned_data['username_id']).username
        if self.cleaned_data['groupname_id']:
            tmp_groupname = Ftpgroup.objects.get(pk=self.cleaned_data['groupname_id']).groupname
        item_string = tmp_username + tmp_groupname + fix_path( self.cleaned_data.get('path', '') )
        item_string_list = [ s_item[0]+s_item[1]+s_item[2] for s_item in self.model.objects.all().values_list('username', 'groupname', 'path') ]
        if item_string in item_string_list:
            if self.instance:
                if self.instance.path != fix_path( self.cleaned_data.get('path', '') ):
                    raise forms.ValidationError(_('You must choice another username + path or groupname + path !'))
                    return False
            else:
                raise forms.ValidationError(_('You must choice another username + path or groupname + path !'))
                return False
        else:
            return True


    def is_username_id_and_groupname_id_null(self):
        if  ( (not self.cleaned_data['username_id']) and (not self.cleaned_data['groupname_id']) ) or  (self.cleaned_data['username_id'] and self.cleaned_data['groupname_id']):
            raise forms.ValidationError(_('You must choice a  username  or a groupname , no both !'))
            return False
        else:
            return True

    def clean_before(self):
        self.is_username_id_and_groupname_id_null()
        self.has_duplicate_ftpacl_item()
