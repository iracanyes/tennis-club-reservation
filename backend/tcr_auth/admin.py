from django.contrib import admin

from .views import AdminEmailLoginForm

# Register custom form with email as identifier
admin.site.login_form = AdminEmailLoginForm

# Register model's classes
#admin.site.register(Admin, UserAdmin)

