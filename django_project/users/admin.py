
# Register your models here.

from django.contrib import admin
from .models import User

class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')

admin.site.register(User)
