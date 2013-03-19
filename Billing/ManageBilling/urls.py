from django.conf.urls import patterns, url
from django.contrib.auth import authenticate
from ManageBilling import auth_views, priv_site_views, manage_objs_view

urlpatterns = patterns('',
				url(r'^$', auth_views.login_view, name = 'login_view'),
				url(r'^customers/(?P<customerID>\d+)/project/(?P<projectID>\d+)$', priv_site_views.project, name='project'),
				url(r'^customers/(?P<customerID>\d+)/project/(?P<projectID>\d+)/create_time/$', manage_objs_view.create_time, name='create_time'),
				url(r'^customers/(?P<customerID>\d+)/contact/(?P<contactID>\d+)$', priv_site_views.contact, name='contact'),
				url(r'^customers/(?P<customerID>\d+)/contact/(?P<contactID>\d+)/create_interaction/$', manage_objs_view.create_interaction, name='create_interaction'),
				url(r'^customers/(?P<customerID>\d+)/create_project/$', manage_objs_view.create_project, name='create_project'),
				url(r'^customers/(?P<customerID>\d+)/create_contact/$', manage_objs_view.create_contact, name='create_contact'),
				url(r'^customers/(?P<customerID>\d+)$', priv_site_views.customers, name='customer'),
				url(r'^customers/', priv_site_views.customers, name='customers'),
				url(r'^register/', auth_views.register, name = 'register'),
				url(r'^logout/$', auth_views.log_out, name = 'logout'),
				url(r'^create_customer/$', manage_objs_view.create_customer, name='create_customer'),
				)