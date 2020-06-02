from django import forms
from django.contrib import auth

from .models import Mess
from accounts.models import City, User


def getCities():
    cities = City.objects.all()
    return cities


categories = [
    ('', ''),
    ('Veg', 'Vegetarian'),
    ('Non-Veg', 'Non-Vegetarian'),
    ('Semi Non-Veg', 'Semi Non-Vegetarian'),
]


class MessForm(forms.Form):
    mess_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'mname', 'oninvalid': "this.setCustomValidity('Please Enter a valid Name')"}))
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control form-control-sm', 'id': 'address', 'oninvalid': "this.setCustomValidity('Please Enter a valid address')"}))
    image_path = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': False, 'class': 'form-control border-0', 'id': 'upload', 'onchange': "readURL(this);"}))
    city = forms.ModelChoiceField(getCities(), widget=forms.Select(attrs={'id': "city", 'class': "form-control form-control-sm", 'oninvalid': "this.setCustomValidity('Please Select a valid City')"}))
    area = forms.IntegerField(widget=forms.Select(attrs={'id': "area", 'class': "form-control form-control-sm", 'oninvalid': "this.setCustomValidity('Please Select a valid Area')"}))


class FoodTypesForm(forms.Form):
    category = forms.ChoiceField(choices=categories, label="Category", widget=forms.Select(attrs={'class': "form-control form-control-md", 'id': 'category',  'oninvalid': "this.setCustomValidity('Please Select Category')"}))
    title = forms.CharField(required=True, label="Title", widget=forms.TextInput(attrs={'class': "form-control form-control-md", 'id': 'title',  'oninvalid': "this.setCustomValidity('Please Enter the Title Name')"}))
    description = forms.CharField(required=True, label="Description", widget=forms.Textarea(attrs={'rows': 3, 'class': "form-control form-control-md", 'id': 'description',  'oninvalid': "this.setCustomValidity('Please Enter the Description')"}))
    price = forms.IntegerField(required=True, label="Price", min_value=0, widget=forms.NumberInput(attrs={'class': "form-control form-control-md", 'id': 'price',  'oninvalid': "this.setCustomValidity('Please Enter Valid Amount')"}))
    image_path = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': False, 'class': 'form-control border-0', 'id': 'upload', 'onchange': "readURL(this);"}))
