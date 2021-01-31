"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(label= _("Логин"),
                               max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Пароль"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class FilterForm (forms.Form):
    date_from = forms.DateTimeField(required=False,
                                    label=_("Начало периода"),
                                    widget=forms.DateTimeInput(
                                            format='%Y-%m-%d %H:%M',
                                            attrs={
                                                'type':'datetime-local'
                                                }), 
                                            localize=True)
    date_to = forms.DateTimeField(required=False,
                                  label=_("Конец периода"),
                                  widget=forms.DateTimeInput(
                                        format='%Y-%m-%d %H:%M', 
                                        attrs={
                                            'type':'datetime-local'
                                            }),
                                        localize=True)
    