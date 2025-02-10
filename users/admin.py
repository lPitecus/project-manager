# Register your models here.
from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user__username", "user__email", "gender", "birth_date", "user__is_superuser"]
    search_fields = ["user__username", "user__email"]
    list_filter = ["gender"]


# Register your models here.
admin.site.register(Profile, ProfileAdmin)
