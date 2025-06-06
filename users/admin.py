from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        (None, {'fields' : ('email', 'password')}),
        ('personal_info', {'fields': ('first_name', 'last_name', 'address', 'phone_number')}),
        ('permissions', {'fields' : ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')})
    )

    add_fieldsets = (
        (None, {
            'classes' : ('wide', ),
            'fields' : ('email', 'password1', 'password2', 'is_staff', 'is_active')
        })
    )

    search_fields = ('email',)
    ordering = ('email',)
admin.site.register(User, CustomUserAdmin)
