# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from . models import Profile

# Register your models here.
class UserProfileInline(admin.StackedInline):
    model = Profile

class UsersAdmin(UserAdmin):
    inlines = [UserProfileInline]

# class ProfileAdmin(admin.ModelAdmin):
#     # list_display = ['user', 'slug']
#     # list_editable = ('slug',)
# admin.site.register(Profile, ProfileAdmin)

admin.site.unregister(User)
admin.site.register(User, UsersAdmin)