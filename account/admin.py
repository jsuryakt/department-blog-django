from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import MyUser, Request

admin.site.register(MyUser)
admin.site.register(Request)
