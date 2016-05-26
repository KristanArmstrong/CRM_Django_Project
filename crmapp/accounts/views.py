from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.shortcuts import render

from .models import Account

class AccountList(ListView):
	model = Account
	paginate_by = 12 #show 12 records at a time
	template_name = 'accounts/account_list.html'
	context_object_name = 'accounts'

	def get_queryset(self):
		#Overrides default behavior to only show records for current user
		try:
			#Check if user is performing a search
			a = self.request.GET.get('account',)
		except KeyError:
			a = None
		if a:
			#If there is a search filter by that value & current user
			account_list = Account.objects.filter(
				name__icontains = a,
				owner = self.request.user
			)
		else:
			#Otherwise return the accounts for current user
			account_list = Account.objects.filter(owner = self.request.user)
		
		return account_list

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		#Protects the view so only authenticated users can access it
		return super(AccountList, self).dispatch(*args, **kwargs)

@login_required
def account_detail(request, uuid):
	#Query database for a given account using UUID (unique identifier for accounts)
	#and display its details
	account = Account.objects.get(uuid = uuid)
	if account.owner != request.user:
		#If current user is not account owner -- return HTTP error 403
		return HttpResponseForbidden()

	variables = {
		'account' : account,
	} #create dictionary of values to be passed into html

	return render(request, 'accounts/account_detail.html', variables)
