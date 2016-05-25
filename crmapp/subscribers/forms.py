from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Subscriber  


class AddressMixin(forms.ModelForm):
	#Subclass of ModelForm need formed based on Subscriber model
    class Meta:
    	#Definition of metadata - required for forms based on ModelForm
        model = Subscriber 
        fields = ('address_one', 'address_two', 'city', 'state',) #fields to be shown
        widgets = {
            'address_one': forms.TextInput(attrs = {'class' : 'form-control'}),
            'address_two': forms.TextInput(attrs = {'class' : 'form-control'}),
            'city': forms.TextInput(attrs = {'class' : 'form-control'}),
            'state': forms.TextInput(attrs = {'class' : 'form-control'}),
        }  #widgets to modify form elements


class SubscriberForm(AddressMixin, UserCreationForm):
	#User firstname field and adding class "form-control" to HTML
	first_name = forms.CharField(
		required = True, widget = forms.TextInput(attrs = {'class' : 'form-control'})
	)
	#User lastname field and adding class "form-control" to HTML
	last_name = forms.CharField(
		required = True, widget = forms.TextInput(attrs = {'class' : 'form-control'})
	)
	#User email field and adding class "form-control" to HTML
	email = forms.EmailField(
		required = True, widget = forms.TextInput(attrs = {'class' : 'form-control'})
	)
	#User username field and adding class "form-control" to HTML
	username = forms.CharField(
		widget = forms.TextInput(attrs = {'class' : 'form-control'})
	)
	#User password field and adding class "form-control" to HTML
	password1 = forms.CharField(
		widget = forms.TextInput(attrs = {'class' : 'form-control', 'type' : 'password'})
	)
	#User password verification field and adding class "form-control" to HTML
	password2 = forms.CharField(
		widget = forms.TextInput(attrs = {'class' : 'form-control', 'type' : 'password'})
	)