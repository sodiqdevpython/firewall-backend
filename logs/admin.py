from django.contrib import admin
from .models import AgentLog

@admin.register(AgentLog)
class AgentLogAdmin(admin.ModelAdmin):
    list_display = ("host", "level", "message")
    list_filter = ("level", "host")
    search_fields = ("message", "host__host_name")