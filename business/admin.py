from django.contrib import admin

from .models import PrimarySector


@admin.register(PrimarySector)
class PrimarySectorAdmin(admin.ModelAdmin):
    list_display = ('name',)