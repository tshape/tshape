from django.contrib import admin

from .models import BaseModel


class BaseModelAdmin(admin.ModelAdmin):

    readonly_fields = ("created_at", "updated_at",)


admin.site.register(BaseModel, BaseModelAdmin)
