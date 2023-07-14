from django import forms
from django.core import validators
from django.contrib.auth.models import User


def check_num_positivo(value):
    if value < 0:
        raise forms.ValidationError("El valor debe ser positivo")


class FormName(forms.Form):
    ref = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),validators=[validators.MaxLengthValidator(25)])
    precioArs = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),validators=[check_num_positivo])


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
