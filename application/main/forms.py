from typing import Sized
from django import forms


class HomeForm(forms.Form):
    post = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Chercher un produit...'
        }
    ))
