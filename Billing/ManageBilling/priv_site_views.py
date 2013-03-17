from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.timezone import utc, get_current_timezone
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from ManageBilling.models import User, Customer
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
	params = {'nav_flag': nav_flag, 'id':customerID}
	if customerID == '':
		customers = Customer.objects.all()
		params['customers'] = customers
		return render(request, 'customers.html', params)
	else:
		customer = Customer.objects.get(pk=customerID)
		params['customer'] = customer
		return render(request, 'customer.html', params)

