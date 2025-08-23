from django.contrib import admin
from .models import FirewallRule


@admin.register(FirewallRule)
class FirewallRuleAdmin(admin.ModelAdmin):
    list_display = ("host", "application", "port", "protocol", "direction", "action")
    list_filter = ("protocol", "direction", "action")
    search_fields = ("host__host_name", "application__name", "port")
