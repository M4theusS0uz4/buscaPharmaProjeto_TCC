from django import forms
from .models import Admin

class AdminGeralForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['username', 'email', 'password', 'id_unidade', 'first_name', 'last_name']

