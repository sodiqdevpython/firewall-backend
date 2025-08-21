from django.contrib import admin
from .models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("host_name", "ip_address", "os_version", "last_seen")
    list_filter = ("status", "os_version")
    search_fields = ("host_name", "ip_address", "bios_uuid")