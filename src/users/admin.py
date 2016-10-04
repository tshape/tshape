from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from profiles.admin import ProfileInline


class UserAdmin(UserAdmin):

    inlines = [ProfileInline]


# admin.site.unregister(User)
admin.site.register(User, UserAdmin)
