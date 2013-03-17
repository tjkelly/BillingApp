from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models.signals import post_save
from django.http import HttpResponse
import datetime
from django.utils.timezone import utc, get_current_timezone

# Create your models here.

class Customer(models.Model):
	name = models.CharField(max_length=200)
	address = models.CharField(max_length=200, blank = True, null = True)

	def __unicode__(self):
		return self.name

class Contact(models.Model):
	name = models.CharField(max_length=200)
	phone = models.CharField(max_length=25, blank = True, null = True)
	email = models.EmailField(max_length=254, blank = True, null = True)
	customer = models.ForeignKey(Customer)

	def __unicode__(self):
		return self.name

class ContactInteraction(models.Model):

	channel_choices = (
		('', 'Select...'),
		('Phone', 'Phone'),
		('Email', 'Email'),
		('In Person', 'In Person'),
		('Other', 'Other'),)

	interaction_channel = models.CharField(max_length = 15,
										choices = channel_choices,
										default='')
	note = models.TextField(max_length=750)
	interaction_date = models.DateField(auto_now = False)
	contact = models.ForeignKey(Contact)

	def __unicode__(self):
		return "Interaction with: " + self.contact.name + ", through " + self.interaction_channel

class Project(models.Model):
	name = models.CharField(max_length=200)
	start_date = models.DateField(auto_now = False)
	end_date = models.DateField(auto_now = False)
	hourly_rate = models.DecimalField(max_digits = 6, decimal_places = 2)
	is_complete = models.BooleanField(default = False)
	estimated_costs = models.DecimalField(max_digits = 6, decimal_places = 2)
	hours_billed_to_date = models.DecimalField(max_digits = 6, decimal_places = 2, blank = True, null = True)
	projected_month_hours =  models.DecimalField(max_digits = 6, decimal_places = 2, blank = True, null = True)
	projected_project_hours = models.DecimalField(max_digits = 6, decimal_places = 2, blank = True, null = True)
	customer = models.ForeignKey(Customer)

	def __unicode__(self):
		return self.name


class BilledTime(models.Model):
	date = models.DateField(auto_now = False)
	num_hours = models.DecimalField(max_digits = 6, decimal_places = 2)
	project = models.ForeignKey(Project)

	def __unicode__(self):
		return self.date + " : " + self.num_hours + " hours"