from django.contrib import admin
from .models import FirewallRule, RuleAssignment

@admin.register(FirewallRule)
class FirewallRuleAdmin(admin.ModelAdmin):
    list_display = ("host", "application", "port", "protocol", "direction", "action")
    list_filter = ("protocol", "direction", "action")
    search_fields = ("host__host_name", "application__name", "port")


@admin.register(RuleAssignment)
class RuleAssignmentAdmin(admin.ModelAdmin):
    list_display = ("rule", "host", "status")
    list_filter = ("status", "host")
    search_fields = ("rule__id", "host__host_name")