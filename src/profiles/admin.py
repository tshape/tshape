from django.contrib import admin

from .models import Profile


class ProfileInline(admin.StackedInline):

    model = Profile


# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)

admin.site.register(Profile)
