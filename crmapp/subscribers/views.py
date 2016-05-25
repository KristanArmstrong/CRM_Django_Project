from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.forms.forms import NON_FIELD_ERRORS
from django.conf import settings
from django.core.urlresolvers import reverse

from .models import Subscriber
from .forms import SubscriberForm

import stripe

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
			fee = settings.SUBSCRIPTION_PRICE
			try:
				stripe_customer = sub.charge(request, email, fee)
			except stripe.StripeError as e:
				form._errors[NON_FIELD_ERRORS] = form.error_class([e.args[0]])
				return render(request, template, 
					{'form': form,
					 'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY}
				)
			#Auto Login
			a_u = authenticate(username = username, password = password) #auth user
			if a_u is not None:
				if a_u.is_active:
					#successful login and returned the account list
					login(request, a_u)
					return HttpResponseRedirect(reverse('account_list'))
				else:
					#redirect to the login page
					return HttpResponseRedirect(
						reverse('django.contrib.auth.views.login')
					)
			else:
				#redirect to the signup page
				return HttpResponseRedirect(reverse('sub_new'))
	else:
		form = SubscriberForm() #user requests subscription for first time

	return render(request, template, 
		{'form' : form,
		 'STRIPE_PUBLISHABLE_KEY' : settings.STRIPE_PUBLISHABLE_KEY}) 
