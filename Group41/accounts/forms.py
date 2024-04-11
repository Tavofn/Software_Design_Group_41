from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User   # using the django default user model
from bootstrap_datepicker_plus.widgets import DatePickerInput

class OrderForm(ModelForm): # name of the model and Form. and inherit from ModelForm.
    class Meta:
        model = Order # which model
        fields = '__all__' # which fields are allowed - ['customer', 'product']. 
    

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']
