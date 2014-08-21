from django.contrib import admin
from server.models import Server

# Register your models here.


class ServerAdmin(admin.ModelAdmin):
    list_display = ['name', 'active','exception', 'modified', 'os', 'os_level', 'centrify', 'xcelys', 'ssl']
    list_filter = ['os', 'os_level', 'active', 'exception', 'centrify', 'xcelys', 'ssl']
    search_fields = ['name', 'os', 'os_level', 'centrify', 'xcelys', 'ssl']
    readonly_fields = ['created', 'modified']
    fields = ['name', 'active', 'exception', 'created', 'modified', 'ip_address', 'os', 'os_level', 'centrify', 'xcelys', 'ssl', 'java', 'log']

admin.site.register(Server, ServerAdmin)
