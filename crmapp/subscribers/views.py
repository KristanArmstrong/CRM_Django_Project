from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from .forms import SubscriberForm
from .models import Subscriber

def subscriber_new(request, template = 'subscribers/subscriber_new.html'):
	if request.method == 'POST':
		form = SubscriberForm(request.POST) #user submitting form
		if form.is_valid():
			#Unpack for values if user submitted valid fields
			username   = form.cleaned_data['username']
			password   = form.cleaned_data['password1']
			email      = form.cleaned_data['email']
			first_name = form.cleaned_data['first_name']
			last_name  = form.cleaned_data['last_name']
			#Create User Record
			user = User(username = username, email = email,
						first_name = first_name, last_name = last_name)
			user.set_password(password)
			user.save()
			#Create Subscriber Record
			address_one = form.cleaned_data['address_one']
			address_two = form.cleaned_data['address_two']
			city        = form.cleaned_data['city']
			state       = form.cleaned_data['state']
			sub         = Subscriber(address_one = address_one, address_two = address_two,
									 city = city, state = state, user_rec = user)
			sub.save()
			#Process Payment (vis Stripe)
			#Auto Login
			return HttpResponseRedirect('/success/')
	else:
		form = SubscriberForm() #user requests subscription for first time

	return render(request, template, {'form' : form}) 
