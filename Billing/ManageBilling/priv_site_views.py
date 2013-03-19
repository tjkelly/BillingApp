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
import calendar
from decimal import *

def return_nav_flag(page):
	nav_flag = {'Home':'', 'Customers':''}
	nav_flag[page] = 'active'
	return nav_flag

def return_this_month_projection(project):
	now = datetime.datetime.now()
	hours_this_month = sum(t.num_hours for t in project.billedtime_set.filter(date__year=now.year, date__month = now.month))
	dollars_this_month = project.hourly_rate * hours_this_month
	avg_hours_per_day = round(Decimal(hours_this_month) / Decimal(now.day), 2)
	est_dollars_left = round(Decimal((calendar.mdays[now.month] - now.day)) * Decimal(avg_hours_per_day) * Decimal(project.hourly_rate), 2)
	est_dollars_total = round(Decimal(dollars_this_month) + Decimal(est_dollars_left), 2)

	return hours_this_month, dollars_this_month, est_dollars_left, est_dollars_total

def return_project_projection(project):
	''' returns the current billed hours and what those hours are worth for the project 
	-- as well as the projected dollars expected to bill (total, and difference left)

	-- assumes that there are no future times billed
	'''
	now = datetime.datetime.now().date()
	total_projected_days = (project.end_date - project.start_date).days
	hours_this_project = sum(t.num_hours for t in project.billedtime_set.all())
	dollars_this_project = hours_this_project * project.hourly_rate
	days_this_project = (now - project.start_date).days
	if days_this_project > 0:
		avg_hours_per_day = round(Decimal(hours_this_project) / Decimal(days_this_project), 2)
		est_dollars_left = round(Decimal((total_projected_days - days_this_project)) * Decimal(avg_hours_per_day) * Decimal(project.hourly_rate), 2)
		est_dollars_total = round(Decimal(dollars_this_project) + Decimal(est_dollars_left), 2)
	else:
		avg_hours_per_day = 0
		est_dollars_total = 0
		est_dollars_left = 0
	return hours_this_project, dollars_this_project, est_dollars_left, est_dollars_total


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
		for customer in customers:
			projects = customer.project_set.all()
			for project in projects:
				project.month_billed_hours_todate, project.month_billed_dollars_todate, project.month_projected_dollars_left, project.month_projected_total_dollars = return_this_month_projection(project)
			customer.month_billed_dollars_todate = sum(p.month_billed_dollars_todate for p in projects)
			customer.month_projected_total_dollars = sum(p.month_projected_total_dollars for p in projects)
		params['customers'] = customers
		return render(request, 'Customer/customers.html', params)
	else:
		customer = Customer.objects.get(pk=customerID)
		projects = customer.project_set.all()
		for project in projects:
			project.month_billed_hours_todate, project.month_billed_dollars_todate, project.month_projected_dollars_left, project.month_projected_total_dollars = return_this_month_projection(project)
			project.project_billed_hours_todate, project.project_billed_dollars_todate, project.project_projected_dollars_left, project.project_projected_total_dollars = return_project_projection(project)
		contacts = customer.contact_set.all()
		params['contacts'] = contacts
		params['customer'] = customer
		params['projects'] = projects
		return render(request, 'Customer/customer.html', params)

@login_required()
def project(request,customerID, projectID=''):
	if projectID == '':
		return customers(request, customerID)
	else:
		nav_flag = return_nav_flag('Customers')
		params = {'nav_flag': nav_flag}
		project = Project.objects.get(pk=projectID)
		project.month_billed_hours_todate, project.month_billed_dollars_todate, project.month_projected_dollars_left, project.month_projected_total_dollars = return_this_month_projection(project)
		project.project_billed_hours_todate, project.project_billed_dollars_todate, project.project_projected_dollars_left, project.project_projected_total_dollars = return_project_projection(project)

		params['project'] = project
		times = project.billedtime_set.all()
		params['times'] = times
		total_time = sum(t.num_hours for t in times)
		params['total_time'] = total_time
		return render(request, 'Project/project.html', params)

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
		return render(request, 'Contact/contact.html', params)


