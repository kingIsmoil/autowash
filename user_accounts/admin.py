from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'fullname', 'is_staff')
    
    list_filter = ('is_staff', 'is_superuser', 'is_active' )
    
    search_fields = ('email', 'fullname','phone_number')

admin.site.register(CustomUser, CustomUserAdmin)