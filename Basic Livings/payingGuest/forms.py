from django import forms
from django.forms import ModelForm
from .models import Room


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control border-0', 'id': 'upload1'}))

