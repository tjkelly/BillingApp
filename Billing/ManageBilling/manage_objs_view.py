from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.timezone import utc, get_current_timezone
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from ManageBilling.models import Customer, Project, BilledTime, Contact, ContactInteraction
from ManageBilling import priv_site_views

@login_required()
def create_customer(request):
	name = request.POST['name']
	address = request.POST['address']
	if (name != '') and (address != ''):
		c= Customer(name= name, address = address)
		c.save()
	return priv_site_views.customers(request)

def create_project(request, customerID):
	cust = Customer.objects.get(pk=customerID)
	name = request.POST['project_name']
	start_date = request.POST['start_date']
	end_date = request.POST['end_date']
	hourly_rate = request.POST['hourly_rate']
	est_costs = request.POST['estimated_costs']
	p = Project(name = name, customer = cust, start_date=start_date, end_date = end_date, hourly_rate = hourly_rate, estimated_costs = est_costs)
	p.save()
	return priv_site_views.customers(request, customerID)

def create_time(request, customerID, projectID):
	proj = Project.objects.get(pk=projectID)
	date = request.POST['date']
	num_hours = request.POST['num_hours']
	t = BilledTime(date = date, num_hours = num_hours, project = proj)
	t.save()
	return priv_site_views.project(request, customerID, projectID)

def create_contact(request, customerID):
	cust = Customer.objects.get(pk=customerID)
	name = request.POST['name']
	email = request.POST['email']
	phone = request.POST['phone']
	cont = Contact(customer = cust, name = name, email= email, phone = phone)
	cont.save()
	return priv_site_views.customers(request, customerID)

def create_interaction(request, customerID, contactID):
	cont = Contact.objects.get(pk=contactID)
	note = request.POST['note']
	channel = request.POST['channel']
	date = request.POST['date']
	interaction = ContactInteraction(contact = cont, interaction_channel = channel, interaction_date = date, note = note)
	interaction.save()
	return priv_site_views.contact(request, customerID, contactID)
