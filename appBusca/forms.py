from django import forms

class BuscaForm(forms.Form):

    query = forms.CharField(label='Buscar', max_length=255)