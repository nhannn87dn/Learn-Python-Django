from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Staff
from django.contrib.auth.models import Permission
#@admin.register(Staff)
class StaffAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser')
    exclude = ('password',)

    
# Register your models here.
admin.site.register(Staff,StaffAdmin)
admin.site.register(Permission)