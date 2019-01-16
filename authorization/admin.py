from django.contrib import admin

from authorization.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdminModel(admin.ModelAdmin):
    pass