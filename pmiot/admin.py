from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from pmiot.models import Archive, Measurement



class ArchiveInline(admin.TabularInline):
    model = Archive

class MeasurementAdmin(admin.ModelAdmin):
    inlines = [
        ArchiveInline,
    ]

admin.site.register(Archive)
admin.site.register(Measurement, MeasurementAdmin)    