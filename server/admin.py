from django.contrib import admin
from server.models import Server
from django.contrib.admin.models import LogEntry

# Register your models here.


class ServerAdmin(admin.ModelAdmin):
    list_max_show_all = 500
    save_on_top = True
    list_display = ['name', 'active','exception', 'modified', 'os', 'os_level', 'centrify', 'xcelys', 'ssl']
    list_filter = ['os', 'os_level', 'active', 'exception', 'centrify', 'xcelys', 'ssl']
    search_fields = ['name', 'os', 'os_level', 'centrify', 'xcelys', 'ssl']
    readonly_fields = ['created', 'modified']
    fields = ['name', 'active', 'exception', 'created', 'modified', 'ip_address', 'os', 'os_level', 'centrify', 'xcelys', 'ssl', 'java', 'log']

class LogEntryAdmin(admin.ModelAdmin):
    """Creating an admin view of the Django contrib auto admin history/log table thingy"""
    
    #note the loss of _id on user_id and content_type_id in the list display
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message')
    list_filter = ('action_time', 'user_id', 'content_type_id')
    search_fields = ('action_time', 'user_id', 'content_type_id', 'object_repr', 'action_flag', 'change_message')
    save_on_top = True
    fields = ('action_time', 'user_id', 'content_type_id', 'object_repr', 'action_flag', 'change_message')
    order = ('-action_time')
    def has_add_permissions(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        #returning false causes table to gray out in the admin page for some reason
        return True
    def has_delete_permission(self, request, obj=None):
        return False



admin.site.register(Server, ServerAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
