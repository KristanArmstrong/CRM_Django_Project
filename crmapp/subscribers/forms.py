from django import forms
from django.contrib.auth.forms import UserCreationForm

class SubscriberForm(UserCreationForm):
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