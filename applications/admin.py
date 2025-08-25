from django.contrib import admin
from .models import Application, Connection
from hosts.models import Device


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("name", "host", "pid",)
    list_filter = ("host",)
    search_fields = ("name", "pid",)


class HostNameFilter(admin.SimpleListFilter):
    title = "Host Name"
    parameter_name = "host_name"

    def lookups(self, request, model_admin):
        hosts = set(Device.objects.values_list("id", "host_name"))
        return [(id, name) for id, name in hosts]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(application__host__id=self.value())
        return queryset


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ("application", "local_address", "remote_address",)
    search_fields = ("local_address", "remote_address")
    list_filter = ("application__host",)
