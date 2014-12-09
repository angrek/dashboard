from django.contrib import admin
from server.models import AIXServer, AIXApplications, DecommissionedAIXServer, Errpt, VIOServer, Power7Inventory, Zone, Stack, Storage, Frame
from server.models import LinuxServer, LinuxApplications, DecommissionedLinuxServer
from server.models import AIXServerResource
from server.models import LinuxServerResource
from server.models import Power7InventoryResource
#from server.models import CapacityPlanning
from django.contrib.admin.models import LogEntry
from import_export.admin import ImportExportModelAdmin

# Register your models here.


#class AIXServerAdmin(admin.ModelAdmin):
class AIXServerAdmin(ImportExportModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=0)
    list_max_show_all = 500
    save_on_top = True
    list_display = ['name', 'owner', 'stack', 'frame', 'zone', 'active','exception', 'modified', 'os', 'os_level', 'emc_clar', 'emc_sym']
    list_filter = ['owner', 'frame', 'os', 'os_level', 'zone', 'active', 'exception', 'emc_clar', 'emc_sym']
    search_fields = ['name', 'owner', 'frame__id', 'os', 'os_level', 'emc_clar', 'emc_sym']
    readonly_fields = ['created', 'modified']
    fields = ['name', 'owner', 'stack', 'frame', 'active', 'exception', 'decommissioned','created', 'modified', 'zone', 'ip_address', 'os', 'os_level', 'emc_clar', 'emc_sym', 'centrify', 'xcelys', 'bash', 'ssl', 'java', 'imperva', 'netbackup', 'log']
    resource_class = AIXServerResource
    #put the js into /home/wrehfiel/ENV/lib/python2.7/site-packages/django/contrib/admin/static/admin/js/
    #there is a copy in the scripts directory so it gets saved into git as well
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    pass

#class AIXApplicationsAdmin(admin.ModelAdmin):
class AIXApplicationsAdmin(ImportExportModelAdmin):
    #def queryset(self, request):
    #    return self.model.objects.filter(name__contains='vio')
    save_on_top = True
    list_display = ['name', 'stack', 'active','exception', 'os', 'os_level', 'zone', 'centrify', 'aix_ssh', 'cent_ssh', 'xcelys', 'bash', 'ssl', 'java', 'imperva', 'netbackup']
    list_filter = ['active', 'exception', 'os', 'os_level', 'zone', 'centrify', 'aix_ssh', 'cent_ssh', 'xcelys', 'bash', 'ssl', 'java', 'imperva', 'netbackup']
    search_fields = ['name', 'os', 'os_level', 'zone__id', 'centrify', 'xcelys', 'bash', 'ssl', 'java', 'imperva', 'netbackup']
    readonly_fields = ['created', 'modified']
    fields = ['name', 'stack', 'active', 'exception', 'decommissioned', 'modified', 'os', 'os_level', 'zone', 'centrify', 'aix_ssh', 'cent_ssh', 'xcelys', 'bash','ssl', 'java', 'imperva', 'netbackup']
    resource_class = AIXServerResource
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    pass

#class AIXServerAdmin(admin.ModelAdmin):
class DecommissionedAIXServerAdmin(ImportExportModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=1)
    list_max_show_all = 500
    save_on_top = True
    list_display = ['name', 'owner', 'frame', 'ip_address', 'zone', 'active','exception', 'modified', 'os', 'os_level', 'emc_clar', 'emc_sym']
    list_filter = ['owner', 'frame', 'os', 'os_level', 'zone', 'active', 'exception', 'emc_clar', 'emc_sym']
    search_fields = ['name', 'owner', 'frame__id', 'ip_address', 'os', 'os_level', 'emc_clar', 'emc_sym']
    readonly_fields = ['created', 'modified']
    fields = ['name', 'owner', 'frame', 'active', 'exception', 'decommissioned', 'created', 'modified', 'zone', 'ip_address', 'os', 'os_level', 'emc_clar', 'emc_sym', 'centrify', 'xcelys', 'bash', 'ssl', 'java', 'imperva', 'netbackup', 'log']
    resource_class = AIXServerResource
   #put the js into /home/wrehfiel/ENV/lib/python2.7/site-packages/django/contrib/admin/static/admin/js/
   #there is a copy in the scripts directory so it gets saved into git as well
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    pass

class LinuxServerAdmin(ImportExportModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=0)
    list_max_show_all = 500
    save_on_top = True
    list_display = ['name', 'owner', 'active', 'exception', 'vmware_cluster', 'os', 'os_level', 'ip_address', 'cpu', 'memory', 'storage', 'modified']
    list_filter = ['os', 'owner', 'vmware_cluster', 'os_level', 'active', 'exception']
    search_fields = ['name', 'owner', 'vmware_cluster', 'ip_address', 'os', 'os_level']
    readonly_fields = ['created', 'modified']
    fields = ['name', 'owner', 'vmware_cluster', 'ip_address', 'active', 'exception', 'decommissioned', 'created', 'modified', 'cpu', 'memory', 'storage', 'os', 'os_level', 'centrify', 'xcelys', 'bash', 'ssl', 'java', 'imperva', 'netbackup', 'log']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    resource_class = LinuxServerResource
    pass

class DecommissionedLinuxServerAdmin(ImportExportModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=1)
    list_max_show_all = 500
    save_on_top = True
    list_display = ['name', 'owner', 'active', 'exception', 'vmware_cluster', 'os', 'os_level', 'ip_address', 'cpu', 'memory', 'storage', 'modified']
    list_filter = ['os', 'owner', 'vmware_cluster', 'os_level', 'active', 'exception']
    search_fields = ['name', 'owner', 'vmware_cluster', 'ip_address', 'os', 'os_level']
    readonly_fields = ['created', 'modified']
    fields = ['name', 'owner', 'vmware_cluster', 'ip_address', 'active', 'exception', 'decommissioned', 'created', 'modified', 'cpu', 'memory', 'storage', 'os', 'os_level', 'centrify', 'xcelys', 'bash', 'ssl', 'java', 'imperva', 'netbackup', 'log']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    resource_class = LinuxServerResource
    pass

class LinuxApplicationsAdmin(ImportExportModelAdmin):
    save_on_top = True
    list_display = ['name', 'active','exception', 'os', 'os_level', 'zone', 'centrify', 'xcelys', 'bash', 'ssl', 'java', 'imperva', 'netbackup']
    list_filter = ['active', 'exception', 'os', 'os_level', 'zone', 'centrify', 'xcelys', 'bash', 'ssl', 'java', 'imperva', 'netbackup']
    search_fields = ['name', 'os', 'os_level', 'zone', 'centrify', 'xcelys', 'bash', 'ssl', 'java', 'imperva', 'netbackup']
    readonly_fields = ['created', 'modified']
    fields = ['name', 'active', 'exception', 'modified', 'os', 'os_level', 'zone', 'centrify', 'xcelys', 'bash','ssl', 'java', 'imperva', 'netbackup']
    resource_class = LinuxServerResource
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    pass


#FIXME put 'frames back into aixserver and vioserver classes
#class VIOServerAdmin(admin.ModelAdmin):
class VIOServerAdmin(ImportExportModelAdmin):
    #FIXME why was this pass here??
    #pass
    def get_queryset(self, request):
        return self.model.objects.filter(name__contains='vio')
    save_on_top = True
    list_display = ['name', 'frame', 'active','exception', 'modified', 'os', 'os_level', 'centrify', 'xcelys', 'bash', 'ssl']
    list_filter = ['os', 'frame', 'os_level', 'active', 'exception', 'centrify', 'xcelys', 'bash', 'ssl']
    search_fields = ['name', 'os', 'os_level', 'centrify', 'xcelys', 'bash', 'ssl']
    readonly_fields = ['created', 'modified']
    fields = ['name', 'frame', 'active', 'exception', 'created', 'modified', 'ip_address', 'os', 'os_level', 'centrify', 'xcelys', 'bash','ssl', 'java', 'log']
    resource_class = AIXServerResource
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    pass

class Power7InventoryAdmin(ImportExportModelAdmin):
    list_max_show_all = 500
    save_on_top = True
    list_display = ('name', 'lpar_id', 'curr_shared_proc_pool_name', 'curr_min_proc_units', 'curr_proc_units', 'curr_max_proc_units', 'curr_min_mem', 'curr_mem', 'curr_max_mem')
    list_filter = ('curr_shared_proc_pool_name', 'curr_min_proc_units', 'curr_proc_units', 'curr_max_proc_units', 'curr_min_mem', 'curr_mem', 'curr_max_mem')
    search_fields = ('name', 'lpar_id', 'curr_shared_proc_pool_name', 'curr_min_proc_units', 'curr_proc_units', 'curr_max_proc_units', 'curr_min_mem', 'curr_mem', 'curr_max_mem')
    fields = ('name', 'lpar_id', 'curr_shared_proc_pool_name', 'curr_min_proc_units', 'curr_proc_units', 'curr_max_proc_units', 'curr_min_mem', 'cur_mem', 'max_mem')

    resource_class = Power7InventoryResource
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    pass




class LogEntryAdmin(admin.ModelAdmin):
    """Creating an admin view of the Django contrib auto admin history/log table thingy"""
    #note the loss of _id on user_id and content_type_id in the list display
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message')
    list_filter = ('action_time', 'user_id', 'content_type_id')
    #search_fields = ( 'user_id', 'content_type', 'object_repr', 'action_flag', 'change_message')
    search_fields = ('user__id', 'content_type__id', 'object_repr', 'change_message',)
    save_on_top = True
    #fields = ('id', 'action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message')
    order = ('-action_time')
    def has_add_permissions(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        #returning false causes table to gray out in the admin page for some reason
        return True
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']




class ErrptAdmin(admin.ModelAdmin):
    list_display = ['name', 'modified', 'report']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']

class ZoneAdmin(admin.ModelAdmin):
    list_display = ['name',]
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']

class StackAdmin(admin.ModelAdmin):
    list_display = ['name',]
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']

class FrameAdmin(admin.ModelAdmin):
    list_display = ['name',]
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']

class StorageAdmin(admin.ModelAdmin):
    list_display = ['name', 'size']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']


admin.site.register(AIXServer, AIXServerAdmin)
admin.site.register(AIXApplications, AIXApplicationsAdmin)
admin.site.register(DecommissionedAIXServer, DecommissionedAIXServerAdmin)
admin.site.register(LinuxServer, LinuxServerAdmin)
admin.site.register(LinuxApplications, LinuxApplicationsAdmin)
admin.site.register(DecommissionedLinuxServer, DecommissionedLinuxServerAdmin)
admin.site.register(VIOServer, VIOServerAdmin)
admin.site.register(Power7Inventory, Power7InventoryAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(Errpt, ErrptAdmin)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(Stack, StackAdmin)
admin.site.register(Frame, FrameAdmin)
admin.site.register(Storage, StorageAdmin)
