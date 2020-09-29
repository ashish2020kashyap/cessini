from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *
from django import forms
from django.forms import ModelForm



class CreateUserForm(UserCreationForm):
    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2',]



class CampaignForm(ModelForm):
    class Meta:
        model = Campaign
        fields = '__all__'



class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user','name','phone','customer_email']

class EmailForm(ModelForm):
    class Meta:
        model = Email
        fields = '__all__'


class EmailUpdateForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user','name','phone','customer_camp']


class CampUpdateForm(ModelForm):
    class Meta:
        model = Campaign
        fields = '__all__'
        exclude = ['my_customer']
