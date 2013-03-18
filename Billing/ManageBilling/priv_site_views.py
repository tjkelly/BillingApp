from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.timezone import utc, get_current_timezone
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from ManageBilling.models import User, Customer, Project, Contact
import datetime

def return_nav_flag(page):
	nav_flag = {'Home':'', 'Customers':''}
	nav_flag[page] = 'active'
	return nav_flag

@login_required()
def home(request):
	nav_flag = return_nav_flag('Home')
	params = {'nav_flag':nav_flag}
	return render(request, 'home.html', params)



@login_required()
def customers(request, customerID=''):
	nav_flag = return_nav_flag('Customers')
	params = {'nav_flag': nav_flag}
	if customerID == '':
		customers = Customer.objects.all()
		params['customers'] = customers
		return render(request, 'customers.html', params)
	else:
		customer = Customer.objects.get(pk=customerID)
		projects = customer.project_set.all()
		contacts = customer.contact_set.all()
		params['contacts'] = contacts
		params['customer'] = customer
		params['projects'] = projects
		return render(request, 'customer.html', params)

@login_required()
def project(request,customerID, projectID=''):
	if projectID == '':
		return customers(request, customerID)
	else:
		nav_flag = return_nav_flag('Customers')
		params = {'nav_flag': nav_flag}
		project = Project.objects.get(pk=projectID)
		params['project'] = project
		times = project.billedtime_set.all()
		params['times'] = times
		total_time = sum(t.num_hours for t in times)
		params['total_time'] = total_time
		return render(request, 'project.html', params)

@login_required()
def contact(request, customerID, contactID=''):
	if contactID == '':
		return customers(request, customerID)
	else:
		nav_flag = return_nav_flag('Customers')
		params = {'nav_flag':nav_flag}
		customer = Customer.objects.get(pk=customerID)
		params['customer'] = customer
		contact = Contact.objects.get(pk=contactID)
		params['contact'] = contact
		interactions = contact.contactinteraction_set.all()
		params['interactions'] = interactions
		return render(request, 'contact.html', params)


