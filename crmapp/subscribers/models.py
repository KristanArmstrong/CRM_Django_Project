from django.db import models
from django.contrib.auth.models import User

class Subscriber(models.Model):
	#Defining the columns/attributes of the table
	user_rec    = models.ForeignKey(User) #foreign key relationship to the User model
	address_one = models.CharField(max_length = 100)
	address_two = models.CharField(max_length = 100, blank = True)
	city        = models.CharField(max_length = 50)
	state       = models.CharField(max_length = 2)
	stripe_id   = models.CharField(max_length = 30, blank = True)

	class Meta:
		#Giving the model metadata - defining the plural name of the class
		verbose_name_plural = 'subscribers'

	def __unicode__(self):
		#Defines the unicode representation of objects in model
		return u"%s's Subscription Info" % self.user_rec

