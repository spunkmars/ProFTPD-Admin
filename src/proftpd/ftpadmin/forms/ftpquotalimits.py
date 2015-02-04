#coding=utf-8
import datetime
from django import forms
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple, SplitDateTimeWidget
from django.forms.extras.widgets import SelectDateWidget
from django.db.models.fields import BLANK_CHOICE_DASH
from django.utils.translation import ugettext_lazy as _

from proftpd.ftpadmin.lib.form_common import newModelForm, set_select_choice, EXPIRATION_YEAR_CHOICES
from proftpd.ftpadmin.models.ftpquotalimits import Ftpquotalimits


class QuotaLimitsForm(newModelForm):
    username_id = forms.ChoiceField(choices=(), label=_('The Name of user')+' :')
    username = forms.CharField( widget=forms.HiddenInput(), required=False)
    quota_type = forms.ChoiceField( choices=(),  label=_('quota_type')+' :')
    per_session = forms.ChoiceField( choices=(), label=_('per_session')+' :')
    limit_type = forms.ChoiceField( choices=(),  label=_('limit_type')+' :')
    bytes_in_avail = forms.DecimalField( max_digits=20, label=_('bytes_in_avail')+' :')
    bytes_out_avail = forms.DecimalField( max_digits=20, label=_('bytes_out_avail')+' :')
    bytes_xfer_avail = forms.DecimalField( max_digits=20, label=_('bytes_xfer_avail')+' :')
    files_in_avail = forms.DecimalField( max_digits=20, label=_('files_in_avail')+' :')
    files_out_avail  = forms.DecimalField( max_digits=20, label=_('files_out_avail')+' :')
    files_xfer_avail = forms.DecimalField(max_digits=20, label=_('files_xfer_avail')+' :')

    def init_after(self):

        if self.instance:
            choices=((self.instance.username_id.id, self.instance.username_id.__unicode__()),)
            self.fields['username_id'].choices = set_select_choice(choices=choices, select_choice=self.instance.username_id.id)
        else:
            field_object = self.model._meta.get_field_by_name('username_id')[0]
            pk_list = [ pk_value[0] for pk_value in field_object.related.parent_model.objects.all().values_list('id') ]
            not_list = [ pk_value[0] for pk_value in self.model.objects.all().values_list('username_id') ]
            choices = [ (pk_value, field_object.related.parent_model.objects.get( pk=pk_value).__unicode__() ) for pk_value in pk_list if pk_value not in not_list]
            choices =  BLANK_CHOICE_DASH + list(choices)
            self.fields['username_id'].choices = set_select_choice(choices=choices, select_choice='')
