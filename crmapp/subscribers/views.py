from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from .forms import SubscriberForm

def subscriber_new(request, template = 'subscribers/subscriber_new.html'):
	if request.method == 'POST':
		form = SubscriberForm(request.POST) #user submitting form
		if form.is_valid():
			#Unpack for values if user submitted valid fields
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			email    = form.cleaned_data['email']
			#Create User Record
			user = User(username = username, email = email)
			user.set_password(password)
			user.save()
			#Create Subscriber Record
			#Process Payment (vis Stripe)
			#Auto Login
			return HttpResponseRedirect('/success/')
	else:
		form = SubscriberForm() #user requests subscription for first time

	return render(request, template, {'form' : form}) 
