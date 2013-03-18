from django.conf.urls import patterns, url
from django.contrib.auth import authenticate
from ManageBilling import auth_views, priv_site_views

urlpatterns = patterns('',
				url(r'^$', auth_views.login_view, name = 'login_view'),
				url(r'^customers/(?P<customerID>\d+)/project/(?P<projectID>\d+)$', priv_site_views.project, name='project'),
				url(r'^customers/(?P<customerID>\d+)/contact/(?P<contactID>\d+)$', priv_site_views.contact, name='contact'),
				url(r'^customers/(?P<customerID>\d+)$', priv_site_views.customers, name='customer'),
				url(r'^customers/', priv_site_views.customers, name='customers'),
				url(r'^register/', auth_views.register, name = 'register'),
				url(r'^logout/$', auth_views.log_out, name = 'logout'),
				)