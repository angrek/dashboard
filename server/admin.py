from django.contrib import admin
from server.models import AIXServer, AIXApplications, DecommissionedAIXServer, Errpt, VIOServer, Power7Inventory, Zone, Stack, SubStack, Storage, Frame, AIXMksysb, AIXPowerHA
from server.models import AIXServerResource
from server.models import AIXServerENV
from server.models import AIXProcPool
from server.models import AIXAffinity
from server.models import AIXWorldWideName
from server.models import AIXServerOwner
from server.models import Power7InventoryResource
from server.models import Relationships

from server.models import Java
from server.models import OracleDatabase

from server.models import LarrysFat

from server.models import LinuxServer
from server.models import LinuxApplications
from server.models import LinuxServerResource
from server.models import LinuxServerENV
from server.models import DecommissionedLinuxServer


from server.models import HistoricalAIXData
from server.models import HistoricalAIXProcPoolData
from server.models import HistoricalPowerInventory
from server.models import HistoricalLinuxData
from server.models import HistoricalWindowsData

from server.models import LocalUser
from server.models import CentrifyUser
from server.models import CentrifyUserCountAIX
from server.models import CentrifyUserCountLinux

#Stupid windows testing.
from server.models import WindowsServer
from server.models import WindowsServerOwner
from server.models import WindowsServerResource
from server.models import DecommissionedWindowsServer

from django.contrib.admin.models import LogEntry

#Excel stuff
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin


# Register your models here.

class RelationshipsInline(admin.TabularInline):
    model = Relationships
    fk_name = 'parent_lpar'
    extra = 2

class AIXLogAdmin(admin.TabularInline):
#    model = AIXServer
    def get_queryset(self, request):
        return self.model.objects.get_history()

######################### AIX Server Section #############################
##########################################################################

class AIXServerAdmin(ImportExportActionModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=0)

    #This overrides the cell div and sets it to a color based on what stack a server is in
    #Note: var was 'stack_color' which displayed as 'Stack color' which was overly wide
    #in the list display. The underscore converts to a space, but I couldn't use just 'stack'
    #without it interferring with the stack object, so I used the _ at the end since it
    #just translates to a space and is not visible in the list_display header.
    def stack_(self, obj):
        if str(obj.stack) == 'Orange':
            return '<div style="width:100%%; background-color:#E97451;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Green':
            return '<div style="width:100%%; background-color:#87A96B;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Yellow':
            return '<div style="width:100%%; background-color:#FFEE77;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Red':
            return '<div style="width:100%%; background-color:#A52A2A;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Train':
            return '<div style="width:100%%; background-color:#72A0C1;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Config':
            return '<div style="width:100%%; background-color:#CD9575;">%s</div>' % obj.stack.name
        else:
            return obj.stack
    stack_.allow_tags = True

    list_max_show_all = 1500
    save_on_top = True
    list_display = ['name', 'image_tag', 'owner', 'application', 'stack_', 'substack',  'frame', 'zone', 'active','exception', 'os', 'os_level', 'asm', 'ifix', 'efix', 'tmef', 'emc_clar', 'emc_sym','centrify_user_count']
    list_filter = ['active', 'exception', 'zone', 'stack', 'substack', 'os', 'os_level', 'asm', 'ifix', 'efix', 'tmef', 'emc_clar', 'emc_sym', 'owner', 'application']
    search_fields = ['name', 'owner', 'application', 'frame__name', 'os', 'os_level', 'emc_clar', 'emc_sym']
    readonly_fields = ['created', 'modified', 'image_tag']
    fields = ['name', 'image_tag', ['owner', 'application', 'stack', 'substack'], 'frame', ['active', 'exception', 'decommissioned'],['created', 'modified'], ['zone', 'asm', 'ifix', 'efix'], ['os', 'os_level'], 'tmef', 'emc_clar', 'emc_sym', 'centrify','centrifyda', 'centrify_user_count', 'xcelys', 'bash', 'ssl', 'java', 'imperva', 'netbackup', 'rsyslog', 'samba', 'python', 'server_env', 'server_env_marker', 'server_env_text', 'application_paths', 'local_users']
    inlines = (RelationshipsInline, ) #, AIXLogAdmin)
    resource_class = AIXServerResource
    #put the js into /home/wrehfiel/ENV/lib/python2.7/site-packages/django/contrib/admin/static/admin/js/
    #there is a copy in the scripts directory so it gets saved into git as well

    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    pass

#class AIXApplicationsAdmin(admin.ModelAdmin):
class AIXApplicationsAdmin(ImportExportActionModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=0)
    #This overrides the cell div and sets it to a color based on what stack a server is in
    #See notes in AIXServerAdmin for stack_ variable explanation.
    def stack_(self, obj):
        if str(obj.stack) == 'Orange':
            return '<div style="width:100%%; background-color:#E97451;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Green':
            return '<div style="width:100%%; background-color:#87A96B;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Yellow':
            return '<div style="width:100%%; background-color:#FFEE77;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Red':
            return '<div style="width:100%%; background-color:#A52A2A;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Train':
            return '<div style="width:100%%; background-color:#72A0C1;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Config':
            return '<div style="width:100%%; background-color:#CD9575;">%s</div>' % obj.stack.name
        else:
            return obj.stack
    stack_.allow_tags = True

    list_max_show_all = 1500
    save_on_top = True
    list_display = ['name', 'image_tag', 'owner', 'application', 'stack_', 'substack', 'active','exception', 'os', 'os_level', 'zone', 'centrify', 'centrifyda', 'aix_ssh', 'cent_ssh', 'xcelys', 'bash', 'ssl', 'imperva', 'netbackup', 'rsyslog', 'samba', 'python']
    list_filter = ['active', 'exception', 'zone', 'stack', 'substack', 'os', 'os_level', 'centrify', 'centrifyda', 'aix_ssh', 'cent_ssh', 'xcelys', 'bash', 'ssl', 'imperva', 'netbackup', 'rsyslog', 'samba', 'python', 'owner', 'application']
    search_fields = ['name', 'owner', 'application', 'os', 'os_level', 'zone__id', 'centrify', 'xcelys', 'bash', 'ssl',  'imperva', 'netbackup']
    readonly_fields = ['created', 'modified', 'image_tag']
    fields = ['name', 'image_tag', 'owner', 'application', 'stack', 'substack', 'active', 'exception', 'decommissioned', 'modified', 'os', 'os_level', 'zone', 'centrify', 'centrifyda', 'aix_ssh', 'cent_ssh', 'xcelys', 'bash','ssl', 'java', 'imperva', 'netbackup', 'rsyslog', 'samba', 'python', 'application_paths']
    resource_class = AIXServerResource
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    pass


class AIXServerENVAdmin(ImportExportActionModelAdmin):
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
class AIXPowerHAAdmin(ImportExportActionModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=0).exclude(powerha="None")
    #This overrides the cell div and sets it to a color based on what stack a server is in
    def stack_color(self, obj):
        if str(obj.stack) == 'Orange':
            return '<div style="width:100%%; background-color:#E97451;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Green':
            return '<div style="width:100%%; background-color:#87A96B;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Yellow':
            return '<div style="width:100%%; background-color:#FFEE77;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Red':
            return '<div style="width:100%%; background-color:#A52A2A;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Train':
            return '<div style="width:100%%; background-color:#72A0C1;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Config':
            return '<div style="width:100%%; background-color:#CD9575;">%s</div>' % obj.stack.name
        else:
            return obj.stack
    stack_color.allow_tags = True

    save_on_top = True
    list_display = ['name', 'image_tag', 'zone', 'powerha', 'cluster_description', 'active','exception', 'os', 'os_level', 'owner', 'application']
    list_filter = ['active', 'exception', 'owner', 'application', 'stack', 'os', 'os_level', 'powerha', 'zone']
    #search_fields = ['name_name', 'owner', 'application', 'os', 'os_level', 'zone__id', 'xcelys', 'ssl']
    readonly_fields = ['created', 'modified', 'image_tag']
    fields = ['name', 'image_tag', 'owner', 'application', 'stack', 'active', 'exception', 'decommissioned', 'modified', 'os', 'os_level', 'powerha', 'cluster_description', 'zone']
    resource_class = AIXServerResource
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    pass



#class AIXServerAdmin(admin.ModelAdmin):
class DecommissionedAIXServerAdmin(ImportExportActionModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=1)
    list_max_show_all = 500
    save_on_top = True
    list_display = ['name', 'owner', 'application', 'frame', 'ip_address', 'zone', 'active','exception', 'modified', 'os', 'os_level', 'emc_clar', 'emc_sym']
    list_filter = ['owner', 'application', 'frame', 'os', 'os_level', 'zone', 'active', 'exception', 'emc_clar', 'emc_sym']
    search_fields = ['name', 'owner', 'application', 'frame__id', 'ip_address', 'os', 'os_level', 'emc_clar', 'emc_sym']
    readonly_fields = ['created', 'modified']
    fields = ['name', 'owner', 'application', 'frame', 'active', 'exception', 'decommissioned', 'created', 'modified', 'zone', 'ip_address', 'os', 'os_level', 'emc_clar', 'emc_sym', 'centrify', 'xcelys', 'bash', 'ssl', 'java', 'imperva', 'netbackup', 'application_paths']
    resource_class = AIXServerResource
   #put the js into /home/wrehfiel/ENV/lib/python2.7/site-packages/django/contrib/admin/static/admin/js/
   #there is a copy in the scripts directory so it gets saved into git as well
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    pass

class HistoricalAIXDataAdmin(ImportExportActionModelAdmin):
    list_max_show_all = 500
    save_on_top = True
    list_display = ['date', 'name', 'frame', 'active','exception', 'decommissioned', 'created', 'zone', 'os_level', 'centrify', 'aix_ssh', 'cent_ssh', 'xcelys', 'bash', 'ssl', 'imperva', 'netbackup', 'rsyslog', 'samba', 'python', 'emc_clar', 'emc_sym']
    list_filter = ['date', 'frame', 'active','exception', 'decommissioned', 'zone', 'os_level', 'centrify', 'aix_ssh', 'cent_ssh', 'xcelys', 'bash', 'ssl', 'imperva', 'netbackup', 'rsyslog', 'emc_clar', 'emc_sym']
    search_fields = ['name__name', 'active','exception', 'decommissioned', 'zone__id', 'os_level', 'centrify', 'aix_ssh', 'cent_ssh', 'xcelys', 'bash', 'ssl', 'imperva', 'netbackup', 'emc_clar', 'emc_sym']
    fields = ['date', 'name', 'frame', 'active','exception', 'decommissioned', 'created', 'ip_address', 'zone', 'os_level', 'centrify', 'aix_ssh', 'cent_ssh', 'xcelys', 'bash', 'ssl', 'imperva', 'netbackup', 'rsyslog', 'samba', 'python', 'emc_clar', 'emc_sym']
    resource_class = AIXServerResource
    #put the js into /home/wrehfiel/ENV/lib/python2.7/site-packages/django/contrib/admin/static/admin/js/
    #there is a copy in the scripts directory so it gets saved into git as well

    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    pass

class AIXProcPoolAdmin(ImportExportActionModelAdmin):
    save_on_top = True
    list_display = ['frame', 'pool_name', 'max_proc_units', 'used_proc_units', 'curr_procs', 'modified']
    list_filter = ['frame', 'pool_name', 'modified']
    search_fields = ['frame', 'pool_name', 'max_proc_units', 'used_proc_units', 'curr_procs', 'modified']
    fields = ['frame', 'pool_name', 'max_proc_units', 'used_proc_units', 'curr_procs', 'modified']
    ordering = ['frame']
    class Media:
        js = ['/static/admin/js/list_filter_collaps.js']
    pass

class HistoricalAIXProcPoolAdmin(ImportExportActionModelAdmin):
    save_on_top = True
    list_display = ['date', 'frame', 'pool_name', 'max_proc_units', 'used_proc_units', 'curr_procs']
    list_filter = ['frame', 'pool_name']
    search_fields = ['date', 'frame', 'pool_name', 'max_proc_units', 'used_proc_units', 'curr_procs']
    fields = ['date', 'frame', 'pool_name', 'max_proc_units', 'used_proc_units', 'curr_procs']
    ordering = ['frame']
    class Media:
        js = ['/static/admin/js/list_filter_collaps.js']
    pass

class HistoricalPowerInventoryAdmin(ImportExportActionModelAdmin):
    save_on_top = True
    list_display = ['date', 'name', 'lpar_id', 'frame', 'curr_shared_proc_pool_id', 'curr_proc_units', 'curr_procs', 'curr_mem']
    list_filter = ['frame', ]
    search_fields = ['date', 'frame']
    fields = ['date', 'name', 'lpar_id', 'frame', 'curr_shared_proc_pool_id', 'curr_proc_units', 'curr_procs', 'curr_mem']
    ordering = ['date']
    class Media:
        js = ['/static/admin/js/list_filter_collaps.js']
    pass

class VIOServerAdmin(ImportExportActionModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(name__contains='vio', decommissioned=0)
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

class AIXServerOwnerAdmin(ImportExportActionModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=0)
    list_max_show_all = 500
    save_on_top = True
    list_display = ['name', 'owner', 'application', 'stack', 'substack']
    list_filter = ['os', 'owner', 'application', 'stack', 'substack']
    list_editable = ['owner', 'application', 'stack', 'substack']
    search_fields = ['name', 'owner', 'application', 'stack', 'substack']
    fields = ['name', 'owner', 'application', 'stack', 'substack']
    resource_class = AIXServerResource
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    pass

class Power7InventoryAdmin(ImportExportActionModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=0)

    #This overrides the cell div and sets it to a color based on what stack a server is in
    #Note: var was 'stack_color' which displayed as 'Stack color' which was overly wide
    #in the list display. The underscore converts to a space, but I couldn't use just 'stack'
    #without it interferring with the stack object, so I used the _ at the end since it
    #just translates to a space and is not visible in the list_display header.
    def stack_(self, obj):
        if str(obj.stack) == 'Orange':
            return '<div style="width:100%%; background-color:#E97451;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Green':
            return '<div style="width:100%%; background-color:#87A96B;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Yellow':
            return '<div style="width:100%%; background-color:#FFEE77;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Red':
            return '<div style="width:100%%; background-color:#A52A2A;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Train':
            return '<div style="width:100%%; background-color:#72A0C1;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Config':
            return '<div style="width:100%%; background-color:#CD9575;">%s</div>' % obj.stack.name
        else:
            return obj.stack
    stack_.allow_tags = True

    list_max_show_all = 500
    save_on_top = True
    list_display = ('name', 'frame', 'stack_', 'substack', 'lpar_id', 'active', 'exception', 'modified', 'curr_shared_proc_pool_name', 'curr_min_proc_units', 'curr_proc_units', 'curr_max_proc_units', 'run_procs', 'curr_min_mem', 'curr_mem', 'curr_max_mem')
    list_filter = ('frame', 'active', 'exception', 'stack', 'decommissioned', 'curr_shared_proc_pool_name', 'curr_min_proc_units', 'curr_proc_units', 'curr_max_proc_units', 'run_procs', 'curr_min_mem', 'curr_mem', 'curr_max_mem')
    search_fields = ('name__name', 'lpar_id', 'curr_shared_proc_pool_name', 'curr_min_proc_units', 'curr_proc_units', 'curr_max_proc_units', 'curr_min_mem', 'curr_mem', 'curr_max_mem')
    readonly_fields = ['modified', 'stack']
    fields = ('name', 'frame', 'stack', 'substack', 'lpar_id', 'active', 'exception', 'decommissioned', 'modified', 'curr_shared_proc_pool_name', 'curr_min_proc_units', 'curr_proc_units', 'curr_max_proc_units', 'run_procs', 'curr_min_mem', 'curr_mem', 'curr_max_mem')

    resource_class = Power7InventoryResource
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    pass

class AIXMksysbAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'exists', 'duplicates']
    list_filter = ['date', 'exists', 'duplicates']
    search_fields = ['name', 'date', 'exists', 'duplicates']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']

class AIXWorldWideNameAdmin(admin.ModelAdmin):
    list_display = ['name', 'fiber_channel_adapter', 'world_wide_name1', 'world_wide_name2']
    search_fields = ['name__name', 'fiber_channel_adapter', 'world_wide_name1', 'world_wide_name2']
    fields = ['name', 'fiber_channel_adapter', 'world_wide_name', 'world_wide_name2']
    resource_class = AIXServerResource
    

class ErrptAdmin(admin.ModelAdmin):
    list_display = ['name', 'modified', 'report']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']

class AIXAffinityAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=0, exception=0)
    list_display = ['name', 'frame', 'curr_lpar_score', 'curr_lpar_score_new', 'predicted_lpar_score', 'predicted_lpar_score_new']
    list_filter = ['frame', 'curr_lpar_score', 'predicted_lpar_score']
    search_fields = ['name', 'curr_lpar_score', 'predicted_lpar_score']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']


class LarrysFatAdmin(ImportExportActionModelAdmin):
    list_display = ['project_name', 'requestor', 'approved', 'server_breakdown', 'quote_opex', 'quote_capex', 'total_quote', 'actual_purchase', 'capex', 'opex', 'total_po']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']


#########################Centrify Information########################
#####################################################################

class CentrifyUserCountAIXAdmin(ImportExportModelAdmin):
    list_display = ['run_time', 'name', 'user_count']
    list_filter = ['run_time',]
    search_fields= ['name__name',]
    fields = ['run_time', 'name', 'user_count']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    
class CentrifyUserCountLinuxAdmin(ImportExportModelAdmin):
    list_display = ['run_time', 'name', 'user_count']
    list_filter = ['run_time',]
    search_fields= ['run_time', 'name']
    fields = ['run_time', 'name', 'user_count']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    
class CentrifyUserAdmin(ImportExportModelAdmin):
    list_display = ['username','password', 'uid', 'gid', 'info', 'home_directory', 'shell']
    list_filter = ['gid', 'shell']
    search_fields = ['username','uid', 'gid', 'info', 'home_directory', 'shell']
    fields = ['username','password', 'uid', 'gid', 'info', 'home_directory', 'shell']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    
class LocalUserAdmin(ImportExportModelAdmin):
    list_display = ['username','password', 'uid', 'gid', 'info', 'home_directory', 'shell']
    list_filter = ['gid', 'shell']
    search_fields = ['username','uid', 'gid', 'info', 'home_directory', 'shell']
    fields = ['username','password', 'uid', 'gid', 'info', 'home_directory', 'shell']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    

#########################Linux Server Section#############################
##########################################################################

class LinuxServerAdmin(ImportExportActionModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=0)
    def stack_(self, obj):
        if str(obj.stack) == 'Orange':
            return '<div style="width:100%%; background-color:#E97451;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Green':
            return '<div style="width:100%%; background-color:#87A96B;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Yellow':
            return '<div style="width:100%%; background-color:#FFEE77;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Red':
            return '<div style="width:100%%; background-color:#A52A2A;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Train':
            return '<div style="width:100%%; background-color:#72A0C1;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Config':
            return '<div style="width:100%%; background-color:#CD9575;">%s</div>' % obj.stack.name
        else:
            return obj.stack
    stack_.allow_tags = True

    list_max_show_all = 500
    save_on_top = True
    list_display = ['name', 'owner', 'application', 'stack_', 'active', 'exception', 'zone', 'vmware_cluster', 'adapter', 'os', 'os_level', 'kernel', 'ip_address', 'cpu', 'memory', 'storage', 'modified']
    list_filter = ['active', 'exception', 'zone', 'vmware_cluster', 'os', 'owner', 'application', 'stack', 'vmware_cluster', 'adapter', 'os_level', 'kernel']
    search_fields = ['name', 'owner', 'application', 'ip_address', 'adapter', 'os', 'os_level', 'kernel']
    readonly_fields = ['created', 'modified']
    fields = ['name', 'owner', 'application', 'stack', 'vmware_cluster', 'adapter', 'ip_address', 'active', 'exception', 'decommissioned', 'created', 'modified', 'cpu', 'memory', 'storage', 'zone', 'os', 'os_level', 'kernel', 'centrify', 'centrifyda', 'xcelys', 'bash', 'ssl', 'glibc', 'java', 'netbackup', 'syslog', 'rsyslog', 'rsyslog_r', 'samba', 'python', 'server_env', 'server_env_marker', 'server_env_text', 'application_paths', 'local_users']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    resource_class = LinuxServerResource
    pass

class LinuxApplicationsAdmin(ImportExportActionModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=0)
    list_max_show_all = 500
    save_on_top = True
    list_display = ['name', 'active','exception', 'stack', 'os', 'os_level', 'zone', 'centrify', 'centrifyda', 'xcelys', 'bash', 'ssl', 'glibc', 'netbackup', 'syslog', 'rsyslog', 'rsyslog_r', 'samba', 'python']
    list_filter = ['active', 'exception', 'zone', 'stack', 'os', 'os_level', 'centrify', 'centrifyda', 'xcelys', 'bash', 'ssl', 'glibc', 'netbackup', 'syslog', 'rsyslog', 'rsyslog_r', 'samba', 'python']
    search_fields = ['name', 'os', 'os_level', 'centrify', 'xcelys', 'bash', 'ssl', 'glibc', 'netbackup']
    readonly_fields = ['created', 'modified']
    fields = ['name', 'active', 'exception', 'stack', 'decommissioned', 'modified', 'os', 'os_level', 'zone', 'centrify', 'centrifyda', 'xcelys', 'bash','ssl', 'glibc', 'java', 'netbackup', 'syslog', 'rsyslog', 'rsyslog_r', 'samba', 'python', 'application_paths']
    resource_class = LinuxServerResource
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    pass


class DecommissionedLinuxServerAdmin(ImportExportActionModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=1)
    list_max_show_all = 500
    save_on_top = True
    list_display = ['name', 'owner', 'application', 'active', 'exception', 'vmware_cluster', 'os', 'os_level', 'kernel', 'ip_address', 'cpu', 'memory', 'storage', 'modified']
    list_filter = ['os', 'owner', 'application', 'vmware_cluster', 'os_level', 'kernel', 'active', 'exception']
    search_fields = ['name', 'owner', 'application', 'vmware_cluster', 'ip_address', 'os', 'os_level', 'kernel']
    readonly_fields = ['created', 'modified']
    fields = ['name', 'owner', 'application', 'vmware_cluster', 'ip_address', 'active', 'exception', 'decommissioned', 'created', 'modified', 'cpu', 'memory', 'storage', 'os', 'os_level', 'kernel', 'centrify', 'xcelys', 'bash', 'ssl', 'java', 'netbackup', 'application_paths']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    resource_class = LinuxServerResource
    pass



class HistoricalLinuxDataAdmin(ImportExportActionModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=0)
    list_max_show_all = 500
    save_on_top = True
    list_display = ['date', 'name', 'owner', 'active', 'exception', 'zone', 'vmware_cluster', 'adapter', 'os', 'os_level', 'ip_address', 'cpu', 'memory', 'storage']
    list_filter = ['date', 'os', 'owner', 'vmware_cluster', 'adapter', 'zone', 'os_level', 'active', 'exception']
    search_fields = ['name__name', 'owner', 'ip_address', 'adapter', 'os', 'os_level']
    readonly_fields = ['created', ]
    fields = ['date', 'name', 'owner', 'vmware_cluster', 'adapter', 'ip_address', 'active', 'exception', 'decommissioned', 'created', 'cpu', 'memory', 'storage', 'zone', 'os', 'os_level', 'centrify', 'xcelys', 'bash', 'ssl', 'java', 'netbackup']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    resource_class = LinuxServerResource
    pass





class LinuxServerENVAdmin(ImportExportActionModelAdmin):
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

class SubStackAdmin(admin.ModelAdmin):
    list_display = ['name',]
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']

class FrameAdmin(admin.ModelAdmin):
    list_display = ['name','short_name', 'firmware_version']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']

class JavaAdmin(admin.ModelAdmin):
    list_display = ['name']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']

class OracleDatabaseAdmin(admin.ModelAdmin):
    list_display = ['name']
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

class WindowsServerAdmin(ImportExportActionModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=0)

    #This overrides the cell div and sets it to a color based on what stack a server is in
    def stack_(self, obj):
        if str(obj.stack) == 'Orange':
            return '<div style="width:100%%; background-color:#E97451;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Green':
            return '<div style="width:100%%; background-color:#87A96B;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Yellow':
            return '<div style="width:100%%; background-color:#FFEE77;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Red':
            return '<div style="width:100%%; background-color:#A52A2A;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Train':
            return '<div style="width:100%%; background-color:#72A0C1;">%s</div>' % obj.stack.name
        elif str(obj.stack) == 'Config':
            return '<div style="width:100%%; background-color:#CD9575;">%s</div>' % obj.stack.name
        else:
            return obj.stack
    stack_.allow_tags = True

    list_max_show_all = 1500
    save_on_top = True
    list_display = ['name', 'owner', 'application', 'distribution_list', 'stack_', 'substack', 'active', 'power_state', 'decommissioned', 'zone', 'vmware_cluster', 'adapter', 'os', 'os_level', 'ip_address', 'cpu', 'memory', 'storage', 'modified']
    #list_editable = ['owner', 'stack', 'substack']
    list_filter = ['os', 'owner', 'application', 'distribution_list', 'stack', 'substack', 'vmware_cluster', 'adapter', 'zone', 'os_level', 'active']
    search_fields = ['name', 'owner', 'ip_address', 'adapter', 'zone__id', 'os', 'os_level']
    readonly_fields = ['created', 'modified']
    fields = ['name', 'owner', 'application', 'distribution_list', 'vmware_cluster', 'adapter', 'ip_address', 'stack', 'substack', 'active', 'power_state', 'decommissioned', 'created', 'modified', 'cpu', 'memory', 'storage', 'zone', 'os', 'os_level']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    resource_class = LinuxServerResource
    pass

class DecommissionedWindowsServerAdmin(ImportExportActionModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=1)
    list_max_show_all = 500
    save_on_top = True
    list_display = ['name', 'owner', 'application', 'distribution_list', 'active', 'decommissioned', 'stack', 'substack', 'created', 'modified', 'vmware_cluster', 'adapter', 'ip_address', 'zone', 'os', 'os_level', 'memory', 'cpu', 'storage']
    list_filter = ['os', 'owner', 'application', 'vmware_cluster', 'os_level', 'active']
    search_fields = ['name', 'owner', 'application', 'vmware_cluster', 'ip_address', 'os', 'os_level']
    readonly_fields = ['created', 'modified']
    fields = ['name', 'owner', 'application', 'distribution_list', 'active', 'decommissioned', 'stack', 'substack', 'created', 'modified', 'vmware_cluster', 'adapter', 'ip_address', 'zone', 'os', 'os_level', 'memory', 'cpu', 'storage']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    resource_class = WindowsServerResource
    pass


class WindowsServerOwnerAdmin(ImportExportActionModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(decommissioned=0)
    list_max_show_all = 500
    save_on_top = True
    list_display = ['name', 'owner', 'application', 'distribution_list']
    list_filter = ['os', 'owner', 'application', 'distribution_list']
    list_editable = ['owner', 'application', 'distribution_list']
    search_fields = ['name', 'owner', 'application', 'distribution_list']
    fields = ['name', 'owner', 'application', 'distribution_list']
    class Media:
        js = ['/static/admin/js/list_filter_collapse.js']
    resource_class = WindowsServerResource
    pass

admin.site.register(AIXServer, AIXServerAdmin)
admin.site.register(AIXApplications, AIXApplicationsAdmin)
admin.site.register(HistoricalAIXData, HistoricalAIXDataAdmin)
admin.site.register(DecommissionedAIXServer, DecommissionedAIXServerAdmin)
admin.site.register(Relationships)
admin.site.register(AIXMksysb, AIXMksysbAdmin)
admin.site.register(AIXPowerHA, AIXPowerHAAdmin)
admin.site.register(AIXServerENV, AIXServerENVAdmin)
admin.site.register(AIXAffinity, AIXAffinityAdmin)
admin.site.register(AIXProcPool, AIXProcPoolAdmin)
admin.site.register(AIXWorldWideName, AIXWorldWideNameAdmin)
admin.site.register(AIXServerOwner, AIXServerOwnerAdmin)

admin.site.register(HistoricalAIXProcPoolData, HistoricalAIXProcPoolAdmin)
admin.site.register(HistoricalPowerInventory, HistoricalPowerInventoryAdmin)
admin.site.register(VIOServer, VIOServerAdmin)
admin.site.register(Power7Inventory, Power7InventoryAdmin)
admin.site.register(Errpt, ErrptAdmin)
admin.site.register(Frame, FrameAdmin)

admin.site.register(LinuxServer, LinuxServerAdmin)
admin.site.register(LinuxApplications, LinuxApplicationsAdmin)
admin.site.register(HistoricalLinuxData, HistoricalLinuxDataAdmin)
admin.site.register(DecommissionedLinuxServer, DecommissionedLinuxServerAdmin)
admin.site.register(LinuxServerENV, LinuxServerENVAdmin)

admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(Stack, StackAdmin)
admin.site.register(SubStack, SubStackAdmin)
admin.site.register(Java, JavaAdmin)
admin.site.register(OracleDatabase, OracleDatabaseAdmin)
admin.site.register(Storage, StorageAdmin)
admin.site.register(WindowsServer, WindowsServerAdmin)
admin.site.register(WindowsServerOwner, WindowsServerOwnerAdmin)
admin.site.register(DecommissionedWindowsServer, DecommissionedWindowsServerAdmin)

admin.site.register(CentrifyUserCountAIX, CentrifyUserCountAIXAdmin)
admin.site.register(CentrifyUserCountLinux, CentrifyUserCountLinuxAdmin)
admin.site.register(CentrifyUser, CentrifyUserAdmin)
admin.site.register(LocalUser, LocalUserAdmin)


admin.site.register(LarrysFat, LarrysFatAdmin)
