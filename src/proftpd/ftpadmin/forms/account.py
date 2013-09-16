#coding=utf-8
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(max_length=30, label=_('Username')+' :')
    email = forms.EmailField(label=_('e-Mail')+' :')
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput(render_value=False), label=_('Password')+' :')
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(render_value=False), label=_('Type Password again')+' :')

    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("This username is already in use.Please choose another."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("You must type the same password each time")
        return self.cleaned_data

    def save(self):
        new_user = User.objects.create_user(username=self.cleaned_data['username'],
                                            email=self.cleaned_data['email'],
                                            password=self.cleaned_data['password1'])
        return new_user



class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label=_('Username')+' :')
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(render_value=False), label=_('Password')+' :')
