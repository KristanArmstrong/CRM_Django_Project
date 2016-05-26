from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from .models import Account
from .forms import AccountForm

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

@login_required()
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

@login_required()
def account_cru(request, uuid = None):
	#Create new accounts and edit existing account records
	if uuid:
		#Since UUID is present current user is editing existing account
		account = get_object_or_404(Account, uuid = uuid) #looks up account by UUID
		if account.owner != request.user:
			return HttpResponseForbidden()
	else:
		account = Account(owner = request.owner)

	if request.POST:
		#User is creating new account
		form = AccountForm(request.POST, instance = account) #retrieves user input values
		if form.is_valid():
			#Checks for valid form values 
			account = form.save(commit = False) #saves user data to DB -- not committed
			#By not committing we can set the owner value to current user before saving
			account.owner = request.user
			account.save()
			redirect_url = reverse(
				'crmapp.accounts.views.account_detail',
				args = (account.uuid,)
			)#success - takes user to account detail page
			return HttpResponseRedirect(redirect_url)
	else:
		#User is making a GET request so assign blank form object
		form = AccountForm(instance = account)

	variables = {
		'form' : form,
		'account' : account
	}

	template = 'accounts/account_cru.html'

	return render(request, template, variables) #returns blank new account form
