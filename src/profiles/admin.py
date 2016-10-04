from django.contrib import admin

from profiles.models import Profile


class ProfileInline(admin.StackedInline):

    model = Profile


admin.site.register(Profile)
