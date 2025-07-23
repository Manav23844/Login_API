from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, OTP, RateLimitLog



class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'username', 'is_email_verified', 'is_staff', 'is_active')
    list_filter = ('is_email_verified', 'is_staff', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        (_('Custom fields'), {'fields': ('is_email_verified',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (_('Custom fields'), {'fields': ('is_email_verified',)}),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)



admin.site.register(User, CustomUserAdmin)
admin.site.register(OTP)
admin.site.register(RateLimitLog)
