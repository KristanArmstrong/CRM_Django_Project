from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Account

class AccountList(ListView):
	model = Account
	template_name = 'accounts/account_list.html'
	context_object_name = 'accounts'

	def get_queryset(self):
		#Overrides default behavior to only show records for current user
		account_list = Account.objects.filter(owner = self.request.user)
		return account_list

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		#Protects the view so only authenticated users can access it
		return super(AccountList, self).dispatch(*args, **kwargs)
