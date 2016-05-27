from django import forms

from .models import Communication

class CommunicationForm(forms.ModelForm):
	#Form used to create and edit Communication records
	class Meta:
		model = Communication
		fields = ('subject', 'notes', 'kind', 'date', 'account',)
		widgets = {
			'subject' : forms.TextInput(
				attrs = {
					'placeholder' : 'Subject',
					'class' : 'form-control'
				}
			),
			'notes' : forms.Textarea(
				attrs = {
					'placeholder' : 'Add notes...',
					'class' : 'form-control'
				}
			),
			'kind' : forms.Select(
				attrs = {
					'placeholder' : 'Type',
					'class' : 'form-control'
				}
			),
			'date' : forms.DateInput(
				attrs = {
					'placeholder' : 'Date',
					'class' : 'form-control'
				}
			),
		}