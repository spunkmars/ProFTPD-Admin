#coding=utf-8
import datetime
from django import forms
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple, SplitDateTimeWidget
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext_lazy as _

from proftpd.ftpadmin.lib.form_common import newModelForm, EXPIRATION_YEAR_CHOICES
from proftpd.ftpadmin.models.ftpgroups import Ftpgroup
from proftpd.ftpadmin.settings import  FTP_GROUP_SAFE_GID
from proftpd.ftpadmin.lib.common import check_safe_range


class GroupForm(newModelForm):
    groupname = forms.CharField(max_length=255, label=_('The Name of group')+' :')
    gid       = forms.IntegerField(label=_('The system GID of current group')+' :')
    expiration = forms.CharField(max_length=255, required=False, widget=SelectDateWidget(years=EXPIRATION_YEAR_CHOICES), label=_('Expiration Date')+' :')
    disabled = forms.ChoiceField(choices=(), label=_('Is disabled')+' :')
    description = forms.CharField(widget=forms.Textarea, required=False,  min_length=3, label=_('The Descripiton of current group')+' :')


    def clean_gid(self):
        data_gid = int(self.data['gid'])
        if len(FTP_GROUP_SAFE_GID) == 2:
            if check_safe_range(safe_range=FTP_GROUP_SAFE_GID, c_type="number", v_value=data_gid) != True:
                raise forms.ValidationError(_('You must type a valid  gid !') + "  for example : %s <= gid <= %s ." % (FTP_GROUP_SAFE_GID[0], FTP_GROUP_SAFE_GID[1]) )
            else:
                return data_gid
        else:
            return data_gid

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
