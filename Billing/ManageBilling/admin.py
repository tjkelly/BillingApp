from django.contrib import admin
from ManageBilling.models import Customer, Project, Contact, ContactInteraction, BilledTime

class ProjectInLine(admin.StackedInline):
	model = Project
	extra = 0

class ContactInLine(admin.StackedInline):
	model = Contact
	extra = 0

class CustomerAdmin(admin.ModelAdmin):
	inlines = [ProjectInLine, ContactInLine]

class BilledTimeInline(admin.StackedInline):
	model = BilledTime
	extra = 0

class ProjectAdmin(admin.ModelAdmin):
	inlines = [BilledTimeInline]

class ContactInteractionInline(admin.StackedInline):
	model = ContactInteraction
	extra = 0

class ContactAdmin(admin.ModelAdmin):
	inlines = [ContactInteractionInline]

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Contact, ContactAdmin)
