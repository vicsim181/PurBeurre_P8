from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import User


# class CustomAdmin(UserAdmin):
#     list_display = ('email', 'is_admin')
#     list_filter = ('is_admin',)
#     fieldsets = UserAdmin.fieldsets + (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name')}),
#         ('Permissions', {'fields': ('is_admin',)}),
#     )
#     search_fields = ('email',)
#     ordering = ('email',)


admin.site.register(User)
