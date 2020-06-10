from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import users

class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')

admin.site.register(users, UsersAdmin)