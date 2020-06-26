
# Register your models here.

from django.contrib import admin
from .models import User, ViewedBook

class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')

admin.site.register(User)
admin.site.register(ViewedBook)