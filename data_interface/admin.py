from django.contrib import admin

from . models import Log


# Register your models here.
class LogAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Log._meta.get_fields()]


admin.site.register(Log, LogAdmin)
