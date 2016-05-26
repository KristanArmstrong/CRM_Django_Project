from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import DeleteView

from .models import Contact
from .forms import ContactForm
from crmapp.accounts.models import Account

@login_required()
def contact_detail(request, uuid):
	
	contact = Contact.objects.get(uuid = uuid)

	return render(request,
				  'contacts/contact_detail.html',
				  {'contact' : contact}
	)

@login_required()
def contact_cru(request, uuid = None, account = None):
	#Standard CRUD view (POST:extract info make object, GET:render a blank page)
	###ADDED EDITING BELOW###
	if uuid:
		#if contact already present -- editing 
		contact = get_object_or_404(Contact, uuid = uuid)
		if contact.owner != request.user:
			return HttpResponseForbidden()
	else:
		#create new contact
		contact = Contact(owner = request.user)

	if request.POST:
		form = ContactForm(request.POST, instance = contact)
		if form.is_valid():
			#make sure the user owns the account
			account = form.cleaned_data['account'] ##hidden input element: account ID relating to the contact
			if account.owner != request.user:
				return HttpResponseForbidden()
			#save the data
			contact 	  = form.save(commit = False)
			contact.owner = request.user
			contact.save()
			#return the user to the account detail view
			if request.is_ajax():
				#returns content_item template instead of entire page
				return render(request,
					'contacts/contact_item_view.html',
					{'account' : account, 'contact' : contact}
				)
			else:
				reverse_url = reverse(
					'crmapp.accounts.views.account_detail',
					args = (account.uuid,)
				)
				return HttpResponseRedirect(reverse_url)
		else:
			#if the form isn't valid, still fetch the account so it can be passed to 
			#the template
			account = form.cleaned_data['account']
	else:
		form = ContactForm(instance = contact)

	#this is used to fetch the account if it exists as a URL parameter
	if request.GET.get('account', ''):
		account = Account.objects.get(id = request.GET.get('account', ''))

	variables = {
		'form' : form,
		'contact' : contact,
		'account' : account
	}

	if request.is_ajax():
		#returns the contact_item_form -- not entire contact_cru page
		template = 'contacts/contact_item_form.html'
	else:
		template = 'contacts/contact_cru.html'

	return render(request, template, variables)

class ContactMixin(object):
	model = Contact

	def get_context_data(self, **kwargs):
		#Giving the object_name variable the correct name
		kwargs.update({'object_name' : 'Contact'})
		return kwargs

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		#REQUIRED dispatch method w/ custom mixin
		return super(ContactMixin, self).dispatch(*args, **kwargs)

class ContactDelete(ContactMixin, DeleteView):
	template_name = 'object_confirm_delete.html'

	def get_object(self, queryset = None):
		obj = super(ContactDelete, self).get_object()
		if not obj.owner == self.request.user:
			raise Http404
		account = Account.objects.get(id = obj.account.id) #need related account to render HTML
		self.account = account
		return obj

	def get_success_url(self):
		#Direct the user back to the Account Detail page
		return reverse(
			'crmapp.accounts.views.account_detail',
			args = (self.account.uuid,)
		)
