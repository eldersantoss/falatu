from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    filter_horizontal = ["following"]
