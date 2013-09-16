#coding=utf-8
import datetime
from django import forms
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple, SplitDateTimeWidget
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext_lazy as _

from proftpd.ftpadmin.lib.form_common import newModelForm, EXPIRATION_YEAR_CHOICES
from proftpd.ftpadmin.settings import FTP_USER_SAFE_HOMEDIR
from proftpd.ftpadmin.models.ftpusers import Ftpuser
from proftpd.ftpadmin.lib.common import check_safe_range, check_invalid_path_format


class UserForm(newModelForm):

    username = forms.CharField(max_length=255, label=_('The Name of user')+' :')
    passwd1 = forms.CharField(max_length=255, widget=forms.PasswordInput(render_value=False), label=_('The Password of user')+' :')
    passwd = forms.CharField(max_length=255, widget=forms.PasswordInput(render_value=False), label=_('Type Password again')+' :')
    homedir = forms.CharField(max_length=255, label=_('The HOMEDIR of user')+' :')
    shell = forms.ChoiceField(choices=(), required=False, label=_('The System Shell of user')+' :')
    uid       = forms.CharField(label=_('The system UID of current user')+' :', widget=forms.HiddenInput(), required=False,)
    gid       = forms.CharField(label=_('The system GID of current user')+' :', widget=forms.HiddenInput(), required=False,)
    group = forms.ChoiceField(choices=(), label=_('The Group of user')+' :')
    expiration = forms.CharField(max_length=255, required=False, widget=SelectDateWidget(years=EXPIRATION_YEAR_CHOICES), label=_('Expiration Date')+' :')
    disabled = forms.ChoiceField(choices=(), label=_('Is disabled')+' :')
    det_name = forms.CharField(max_length=255, required=False, label=_('The Full Name of user')+' :')
    det_mail = forms.EmailField(max_length=255, required=False, label=_('The E-Mail of user')+' :')
    det_address = forms.CharField(max_length=255, required=False, label=_('The Det Address of user')+' :')
    det_notes = forms.CharField(widget=forms.Textarea, required=False,  min_length=3, label=_('The Descripiton of current user')+' :')

    def init_edit_form(self):
        self.fields['passwd1'].required=False
        self.fields['passwd'].required=False

    def clean_passwd(self):
        if self.cleaned_data['passwd1'] != '' or  self.cleaned_data['passwd'] != '' :
            if self.cleaned_data['passwd1'] != self.cleaned_data['passwd']:
                raise forms.ValidationError(_('You mast type the same password each time!'))
            else:
                return self.cleaned_data['passwd']
        elif self.instance != None:
            return self.instance.passwd

    def clean_homedir(self):
        has_invalid_format = False
        has_unsafe_path = False
        if check_invalid_path_format(self.cleaned_data['homedir']):
            has_invalid_format = True
            raise forms.ValidationError(_('You must type a valid  homedir!') + "  Make sure the homedir not contains a special string (../ or ./ or // or /.) ")
        else:
            has_invalid_format = False

        if len(FTP_USER_SAFE_HOMEDIR):
            safe_homedir_string = '"' + '", "'.join(FTP_USER_SAFE_HOMEDIR) + '"'
            if check_safe_range(safe_range=FTP_USER_SAFE_HOMEDIR, c_type="startswith", v_value=self.cleaned_data['homedir']) == True:
                has_unsafe_path = False
            else:
                has_unsafe_path = True
                raise forms.ValidationError(_('You must type a valid  homedir!') + "  for example : %s ." % safe_homedir_string)
        else:
            has_unsafe_path = False

        if has_invalid_format == False and has_unsafe_path == False:
            return  self.cleaned_data['homedir']

        
    def clean_expiration(self):
        
        if self.data != None:
            expiration_year = int(self.data['expiration_year'])
            expiration_month = int(self.data['expiration_month'])
            expiration_day = int(self.data['expiration_day'])
            if expiration_year != 0 and  expiration_month != 0 and expiration_day != 0 :
                expiration_datetime = datetime.date(expiration_year, expiration_month, expiration_day).strftime('%Y-%m-%d %X')
                return expiration_datetime
            else:
                if self.instance != None:
                    return self.instance.expiration
                else:
                    expiration_datetime = datetime.date(2110, 12,31).strftime('%Y-%m-%d %X')
                return expiration_datetime




    