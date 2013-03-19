# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.timezone import utc, get_current_timezone
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from ManageBilling.models import User
from ManageBilling import priv_site_views
import datetime

def login_view(request):
	if request.method == 'POST':
		user = authenticate(username = request.POST['username'], password = request.POST['password'])
		if user is not None:
			if user.is_active:
				#request.session['user'] = user
				login(request, user)
				return priv_site_views.home(request)
			else:
				return render(request, 'Auth/login_page.html', {'error_message':'Your account has been disabled'})
		else:
			return render(request, 'Auth/login_page.html', {'error_message':"Your user name or password don't match our records"})
	elif request.user.is_authenticated():
		return priv_site_views.home(request)
	else:
		return render(request, 'Auth/login_page.html')

def log_out(request):
	logout(request)
	return login_view(request)

def register(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		email = request.POST['email']
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']

		if username == '' or password == '' or email == '':
			return render(request, 'Auth/registration_page.html', {'error_message':"A required field has been left empty!",})

		try:
			user = User.objects.get(username = username)
		except (KeyError,User.DoesNotExist):
			# Add in e-mail authentication!
			user = User.objects.create_user(username, email, password)
			user.first_name = first_name
			user.last_name = last_name
			user.full_name = first_name + " " + last_name
			user.save()
			user = authenticate(username=username, password=password)
			login(request, user)
			return render(request, 'Auth/login_page.html', {'success_message':"You successfully registered!",})
		else:
			return render(request, 'Auth/registration_page.html', {'error_message':"Username already exists!",})
	else:
		return render(request, 'Auth/registration_page.html')