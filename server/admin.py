from django.contrib import admin
from server.models import AIXServer, AIXApplications, DecommissionedAIXServer, Errpt, VIOServer, Power7Inventory, Zone, Stack, Storage, Frame, AIXMksysb, AIXPowerHA
from server.models import AIXServerResource
from server.models import AIXServerENV

from server.models import LinuxServer, LinuxApplications, DecommissionedLinuxServer
from server.models import LinuxServerResource
from server.models import HistoricalLinuxData
from server.models import LinuxServerENV
from server.models import WindowsServer

from server.models import Power7InventoryResource
#from server.models import Relationships, AIXLog
from server.models import HistoricalAIXData
#from server.models import CapacityPlanning
from django.contrib.admin.models import LogEntry
from import_export.admin import ImportExportModelAdmin


# Register your models here.

#class RelationshipsInline(admin.TabularInline):
#    model = Relationships
#    fk_name = 'parent_lpar'
#    extra = 2

class AIXLogAdmin(admin.TabularInline):
#    model = AIXServer
    def get_queryset(self, request):
        return self.model.objects.get_history()

#class VIOServerAdmin(ImportExportModelAdmin):
#    def get_queryset(self, request):
#            return self.model.objects.filter(name__contains='vio')
#                save_on_top = True
#                    list_display = ['name', 'frame', 'active','exception', 'modified', 'os', 'os_level', 'centrify', 'xcelys', 'bash', 'ssl']
#                        list_filter = ['os', 'frame', 'os_level', 'active', 'exception', 'centrify', 'xcelys', 'bash', 'ssl']
#                            search_fields = ['name', 'os', 'os_level', 'centrify', 'xcelys', 'bash', 'ssl']
#                                readonly_fields = ['created', 'modified']
#                                    fields = ['name', 'frame', 'active', 'exception', 'created', 'modified', 'ip_address', 'os', 'os_level', 'centrify', 'xcelys', 'bash','ssl',
#                                    'java']
#                                        resource_class = AIXServerResource
#                                            class Media:
#                                                    js = ['/static/admin/js/list_filter_collapse.js']
#                                                        pass

######################### AIX Server Section #############################
##########################################################################

class AIXServerAdmin(ImportExportModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=0)

    #This overrides the cell div and sets it to a color based on what stack a server is in
    #Note: var was 'stack_color' which displayed as 'Stack color' which was overly wide
    #in the list display. The underscore converts to a space, but I couldn't use just 'stack'
    #without it interferring with the stack object, so I used the _ at the end since it
    #just translates to a space and is not visible in the list_display header.
    def stack_(self, obj):
        if str(obj.stack) == 'Orange':
            return '<div style="width:100%%; background-color:orange;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Green':
            return '<div style="width:100%%; background-color:green;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Yellow':
            return '<div style="width:100%%; background-color:yellow;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Red':
            return '<div style="width:100%%; background-color:red;">%s</div>' % obj.stack.name
        else:
            return obj.stack
    stack_.allow_tags = True

    list_max_show_all = 1500
    save_on_top = True
    list_display = ['name', 'image_tag', 'owner', 'stack_', 'frame', 'zone', 'active','exception', 'modified', 'ip_address', 'os', 'os_level', 'asm', 'tmef', 'emc_clar', 'emc_sym']
    list_filter = ['stack', 'os', 'os_level', 'zone', 'active', 'exception', 'asm', 'tmef', 'emc_clar', 'emc_sym', 'owner']
    search_fields = ['name', 'owner', 'frame__name', 'ip_address', 'os', 'os_level', 'emc_clar', 'emc_sym']
    readonly_fields = ['created', 'modified', 'image_tag']
    fields = ['name', 'image_tag', ['owner', 'stack'], 'frame', ['active', 'exception', 'decommissioned'],['created', 'modified'], ['zone', 'ip_address', 'asm'], ['os', 'os_level'], 'tmef', 'emc_clar', 'emc_sym', 'centrify', 'xcelys', 'bash', 'ssl', 'java', 'imperva', 'netbackup', 'rsyslog', 'samba', 'server_env', 'server_env_marker', 'server_env_text', 'application_paths']
    #inlines = (RelationshipsInline, ) #, AIXLogAdmin)
    resource_class = AIXServerResource
    #put the js into /home/wrehfiel/ENV/lib/python2.7/site-packages/django/contrib/admin/static/admin/js/
    #there is a copy in the scripts directory so it gets saved into git as well

    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    pass

#class AIXApplicationsAdmin(admin.ModelAdmin):
class AIXApplicationsAdmin(ImportExportModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=0)
    #This overrides the cell div and sets it to a color based on what stack a server is in
    #See notes in AIXServerAdmin for stack_ variable explanation.
    def stack_(self, obj):
        if str(obj.stack) == 'Orange':
            return '<div style="width:100%%; background-color:orange;">%s</div>' % obj.stack
        elif str(obj.stack) == 'Green':
            return '<div style="width:100%%; background-color:green;">%s</div>' % obj.stack
        elif str(obj.stack) == 'Yellow':
            return '<div style="width:100%%; background-color:yellow;">%s</div>' % obj.stack
        elif str(obj.stack) == 'Red':
            return '<div style="width:100%%; background-color:red;">%s</div>' % obj.stack
        else:
            return obj.stack
    stack_.allow_tags = True

    list_max_show_all = 1500
    save_on_top = True
    list_display = ['name', 'image_tag', 'owner', 'stack_', 'active','exception', 'os', 'os_level', 'zone', 'centrify', 'aix_ssh', 'cent_ssh', 'xcelys', 'bash', 'ssl', 'imperva', 'netbackup', 'rsyslog', 'samba']
    list_filter = ['active', 'exception', 'stack', 'os', 'os_level', 'zone', 'centrify', 'aix_ssh', 'cent_ssh', 'xcelys', 'bash', 'ssl', 'imperva', 'netbackup', 'rsyslog', 'samba', 'owner']
    search_fields = ['name', 'owner', 'os', 'os_level', 'zone__id', 'centrify', 'xcelys', 'bash', 'ssl',  'imperva', 'netbackup']
    readonly_fields = ['created', 'modified', 'image_tag']
    fields = ['name', 'image_tag', 'owner', 'stack', 'active', 'exception', 'decommissioned', 'modified', 'os', 'os_level', 'zone', 'centrify', 'aix_ssh', 'cent_ssh', 'xcelys', 'bash','ssl', 'java', 'imperva', 'netbackup', 'rsyslog', 'samba', 'application_paths']
    resource_class = AIXServerResource
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    pass



class AIXServerENVAdmin(ImportExportModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=0)

    save_on_top = True
    list_display = ['name', 'active', 'exception', 'zone', 'server_env', 'server_env_marker', 'server_env_text']
    list_editable = ['server_env_marker',]
    list_filter = ['active', 'exception', 'zone', 'server_env']
    search_fields = ['name', 'zone', 'server_env', 'server_env_text', 'server_env_marker']
    fields = ['name', 'active', 'exception', 'zone', 'server_env', 'server_env_marker', 'server_env_text']

    resource_class = AIXServerResource
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    pass





#class AIXApplicationsAdmin(admin.ModelAdmin):
class AIXPowerHAAdmin(ImportExportModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=0).exclude(powerha="None")
    #This overrides the cell div and sets it to a color based on what stack a server is in
    def stack_color(self, obj):
        if str(obj.stack) == 'Orange':
            return '<div style="width:100%%; background-color:orange;">%s</div>' % obj.stack
        elif str(obj.stack) == 'Green':
            return '<div style="width:100%%; background-color:green;">%s</div>' % obj.stack
        elif str(obj.stack) == 'Yellow':
            return '<div style="width:100%%; background-color:yellow;">%s</div>' % obj.stack
        elif str(obj.stack) == 'Red':
            return '<div style="width:100%%; background-color:red;">%s</div>' % obj.stack
        else:
            return obj.stack
    stack_color.allow_tags = True

    save_on_top = True
    list_display = ['name', 'image_tag', 'owner', 'stack_color', 'active','exception', 'os', 'os_level', 'powerha', 'zone', 'centrify', 'aix_ssh', 'cent_ssh', 'xcelys', 'bash', 'ssl', 'imperva', 'netbackup', 'rsyslog', 'samba']
    list_filter = ['active', 'exception', 'owner', 'stack', 'os', 'os_level', 'powerha', 'zone', 'centrify', 'aix_ssh', 'cent_ssh', 'xcelys', 'bash', 'ssl', 'imperva', 'netbackup', 'rsyslog', 'samba']
    search_fields = ['name', 'owner', 'os', 'os_level', 'zone__id', 'centrify', 'xcelys', 'bash', 'ssl',  'imperva', 'netbackup']
    readonly_fields = ['created', 'modified', 'image_tag']
    fields = ['name', 'image_tag', 'owner', 'stack', 'active', 'exception', 'decommissioned', 'modified', 'os', 'os_level', 'powerha', 'zone', 'centrify', 'aix_ssh', 'cent_ssh', 'xcelys', 'bash','ssl', 'java', 'imperva', 'netbackup','rsyslog', 'samba', 'application_paths']
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
    fields = ['name', 'owner', 'frame', 'active', 'exception', 'decommissioned', 'created', 'modified', 'zone', 'ip_address', 'os', 'os_level', 'emc_clar', 'emc_sym', 'centrify', 'xcelys', 'bash', 'ssl', 'java', 'imperva', 'netbackup', 'application_paths']
    resource_class = AIXServerResource
   #put the js into /home/wrehfiel/ENV/lib/python2.7/site-packages/django/contrib/admin/static/admin/js/
   #there is a copy in the scripts directory so it gets saved into git as well
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    pass

class HistoricalAIXDataAdmin(ImportExportModelAdmin):
    list_max_show_all = 500
    save_on_top = True
    list_display = ['date', 'name', 'frame', 'active','exception', 'decommissioned', 'created', 'zone', 'os_level', 'centrify', 'aix_ssh', 'cent_ssh', 'xcelys', 'bash', 'ssl', 'imperva', 'netbackup', 'rsyslog', 'samba', 'emc_clar', 'emc_sym']
    list_filter = ['date', 'frame', 'active','exception', 'decommissioned', 'zone', 'os_level', 'centrify', 'aix_ssh', 'cent_ssh', 'xcelys', 'bash', 'ssl', 'imperva', 'netbackup', 'rsyslog', 'emc_clar', 'emc_sym']
    search_fields = ['name__name', 'active','exception', 'decommissioned', 'zone__id', 'os_level', 'centrify', 'aix_ssh', 'cent_ssh', 'xcelys', 'bash', 'ssl', 'imperva', 'netbackup', 'emc_clar', 'emc_sym']
    fields = ['date', 'name', 'frame', 'active','exception', 'decommissioned', 'created', 'ip_address', 'zone', 'os_level', 'centrify', 'aix_ssh', 'cent_ssh', 'xcelys', 'bash', 'ssl', 'java', 'imperva', 'netbackup', 'rsyslog', 'samba', 'emc_clar', 'emc_sym']
    resource_class = AIXServerResource
    #put the js into /home/wrehfiel/ENV/lib/python2.7/site-packages/django/contrib/admin/static/admin/js/
    #there is a copy in the scripts directory so it gets saved into git as well

    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    pass


class VIOServerAdmin(ImportExportModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(name__contains='vio')
    save_on_top = True
    list_display = ['name', 'image_tag', 'frame', 'active','exception', 'modified', 'os', 'os_level', 'centrify', 'xcelys', 'bash', 'ssl']
    list_filter = ['os', 'frame', 'os_level', 'active', 'exception', 'centrify', 'xcelys', 'bash', 'ssl']
    search_fields = ['name', 'os', 'os_level', 'centrify', 'xcelys', 'bash', 'ssl']
    readonly_fields = ['created', 'modified', 'image_tag']
    fields = ['name', 'image_tag', 'frame', 'active', 'exception', 'created', 'modified', 'ip_address', 'os', 'os_level', 'centrify', 'xcelys', 'bash','ssl', 'java', 'application_paths']
    resource_class = AIXServerResource
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    pass

class Power7InventoryAdmin(ImportExportModelAdmin):
    list_max_show_all = 500
    save_on_top = True
    list_display = ('name', 'frame', 'lpar_id', 'active', 'exception', 'decommissioned', 'modified', 'curr_shared_proc_pool_name', 'curr_min_proc_units', 'curr_proc_units', 'curr_max_proc_units', 'run_procs', 'curr_min_mem', 'curr_mem', 'curr_max_mem')
    list_filter = ('frame', 'active', 'exception', 'decommissioned', 'curr_shared_proc_pool_name', 'curr_min_proc_units', 'curr_proc_units', 'curr_max_proc_units', 'run_procs', 'curr_min_mem', 'curr_mem', 'curr_max_mem')
    search_fields = ('frame', 'name', 'lpar_id', 'curr_shared_proc_pool_name', 'curr_min_proc_units', 'curr_proc_units', 'curr_max_proc_units', 'curr_min_mem', 'curr_mem', 'curr_max_mem')
    readonly_fields = ['modified',]
    fields = ('name', 'frame', 'lpar_id', 'active', 'exception', 'decommissioned', 'modified', 'curr_shared_proc_pool_name', 'curr_min_proc_units', 'curr_proc_units', 'curr_max_proc_units', 'run_procs', 'curr_min_mem', 'curr_mem', 'curr_max_mem')

    resource_class = Power7InventoryResource
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    pass

class AIXMksysbAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'exists', 'duplicates']
    list_filter = ['date', 'exists', 'duplicates']
    search_field = ['name', 'date', 'exists', 'duplicates']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']


class ErrptAdmin(admin.ModelAdmin):
    list_display = ['name', 'modified', 'report']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']

#########################Linux Server Section#############################
##########################################################################

class LinuxServerAdmin(ImportExportModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=0)
    list_max_show_all = 500
    save_on_top = True
    list_display = ['name', 'owner', 'stack', 'active', 'exception', 'zone', 'vmware_cluster', 'adapter', 'os', 'os_level', 'ip_address', 'cpu', 'memory', 'storage', 'modified']
    list_filter = ['os', 'owner', 'stack', 'vmware_cluster', 'adapter', 'zone', 'os_level', 'active', 'exception']
    search_fields = ['name', 'owner', 'ip_address', 'adapter', 'zone__id', 'os', 'os_level']
    readonly_fields = ['created', 'modified']
    fields = ['name', 'owner', 'stack', 'vmware_cluster', 'adapter', 'ip_address', 'active', 'exception', 'decommissioned', 'created', 'modified', 'cpu', 'memory', 'storage', 'zone', 'os', 'os_level', 'centrify', 'xcelys', 'bash', 'ssl', 'java', 'imperva', 'netbackup', 'syslog', 'rsyslog', 'rsyslog_r', 'samba', 'server_env', 'server_env_marker', 'server_env_text', 'application_paths']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    resource_class = LinuxServerResource
    pass

class LinuxApplicationsAdmin(ImportExportModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=0)
    list_max_show_all = 500
    save_on_top = True
    list_display = ['name', 'active','exception', 'stack', 'os', 'os_level', 'zone', 'centrify', 'xcelys', 'bash', 'ssl', 'imperva', 'netbackup', 'syslog', 'rsyslog', 'rsyslog_r', 'samba']
    list_filter = ['active', 'exception', 'stack', 'os', 'zone', 'os_level', 'zone', 'centrify', 'xcelys', 'bash', 'ssl', 'imperva', 'netbackup', 'syslog', 'rsyslog', 'rsyslog_r', 'samba']
    search_fields = ['name', 'os', 'os_level', 'stack', 'zone__id', 'centrify', 'xcelys', 'bash', 'ssl', 'imperva', 'netbackup']
    readonly_fields = ['created', 'modified']
    fields = ['name', 'active', 'exception', 'stack', 'decommissioned', 'modified', 'os', 'os_level', 'zone', 'centrify', 'xcelys', 'bash','ssl', 'java', 'imperva', 'netbackup', 'syslog', 'rsyslog', 'rsyslog_r', 'samba', 'application_paths']
    resource_class = LinuxServerResource
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
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
    fields = ['name', 'owner', 'vmware_cluster', 'ip_address', 'active', 'exception', 'decommissioned', 'created', 'modified', 'cpu', 'memory', 'storage', 'os', 'os_level', 'centrify', 'xcelys', 'bash', 'ssl', 'java', 'imperva', 'netbackup', 'application_paths']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    resource_class = LinuxServerResource
    pass



class HistoricalLinuxDataAdmin(ImportExportModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=0)
    list_max_show_all = 500
    save_on_top = True
    list_display = ['date', 'name', 'owner', 'active', 'exception', 'zone', 'vmware_cluster', 'adapter', 'os', 'os_level', 'ip_address', 'cpu', 'memory', 'storage']
    list_filter = ['date', 'os', 'owner', 'vmware_cluster', 'adapter', 'zone', 'os_level', 'active', 'exception']
    search_fields = ['name', 'owner', 'ip_address', 'adapter', 'zone__id', 'os', 'os_level']
    readonly_fields = ['created', ]
    fields = ['date', 'name', 'owner', 'vmware_cluster', 'adapter', 'ip_address', 'active', 'exception', 'decommissioned', 'created', 'cpu', 'memory', 'storage', 'zone', 'os', 'os_level', 'centrify', 'xcelys', 'bash', 'ssl', 'java', 'imperva', 'netbackup']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    resource_class = LinuxServerResource
    pass





class LinuxServerENVAdmin(ImportExportModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=0)

    save_on_top = True
    list_display = ['name', 'active', 'exception', 'zone', 'server_env', 'server_env_marker', 'server_env_text']
    list_editable = ['server_env_marker',]
    list_filter = ['active', 'exception', 'zone', 'server_env', 'server_env_marker']
    search_fields = ['name', 'zone', 'server_env', 'server_env_text', 'server_env_marker']
    fields = ['name', 'active', 'exception', 'zone', 'server_env', 'server_env_marker', 'server_env_text']

    resource_class = AIXServerResource
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    pass




class ZoneAdmin(admin.ModelAdmin):
    list_display = ['name',]
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']

class StackAdmin(admin.ModelAdmin):
    list_display = ['name',]
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']

class FrameAdmin(admin.ModelAdmin):
    list_display = ['name','short_name']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']

class StorageAdmin(admin.ModelAdmin):
    list_display = ['name', 'size']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']

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


############################# WINDOWS TESTING ####################################

class WindowsServerAdmin(ImportExportModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=0)
    list_max_show_all = 500
    save_on_top = True
    list_display = ['name', 'owner', 'active', 'exception', 'decommissioned', 'zone', 'vmware_cluster', 'adapter', 'os', 'os_level', 'ip_address', 'cpu', 'memory', 'storage', 'modified']
    list_filter = ['os', 'owner', 'vmware_cluster', 'adapter', 'zone', 'os_level', 'active', 'exception']
    search_fields = ['name', 'owner', 'ip_address', 'adapter', 'zone__id', 'os', 'os_level']
    readonly_fields = ['created', 'modified']
    fields = ['name', 'owner', 'vmware_cluster', 'adapter', 'ip_address', 'active', 'exception', 'decommissioned', 'created', 'modified', 'cpu', 'memory', 'storage', 'zone', 'os', 'os_level']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    resource_class = LinuxServerResource
    pass


admin.site.register(AIXServer, AIXServerAdmin)
admin.site.register(AIXApplications, AIXApplicationsAdmin)
admin.site.register(HistoricalAIXData, HistoricalAIXDataAdmin)
admin.site.register(DecommissionedAIXServer, DecommissionedAIXServerAdmin)

admin.site.register(LinuxServer, LinuxServerAdmin)
admin.site.register(LinuxApplications, LinuxApplicationsAdmin)
admin.site.register(HistoricalLinuxData, HistoricalLinuxDataAdmin)
admin.site.register(DecommissionedLinuxServer, DecommissionedLinuxServerAdmin)

admin.site.register(VIOServer, VIOServerAdmin)
admin.site.register(Power7Inventory, Power7InventoryAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(Errpt, ErrptAdmin)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(Stack, StackAdmin)
admin.site.register(Frame, FrameAdmin)
admin.site.register(Storage, StorageAdmin)
#admin.site.register(Relationships)
admin.site.register(AIXMksysb, AIXMksysbAdmin)
admin.site.register(AIXPowerHA, AIXPowerHAAdmin)
admin.site.register(AIXServerENV, AIXServerENVAdmin)
admin.site.register(LinuxServerENV, LinuxServerENVAdmin)
admin.site.register(WindowsServer, WindowsServerAdmin)
