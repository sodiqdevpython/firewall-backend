from django.contrib import admin
from .models import Application, Connection

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("name", "host", "pid", "status", "hash")
    list_filter = ("status", "host")
    search_fields = ("name", "pid", "hash")

@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ("application", "protocol", "local_address", "remote_address",)
    list_filter = ("protocol",)
    search_fields = ("local_address", "remote_address")