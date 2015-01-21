from django.db import models
from django.contrib.auth.models import User
import datetime
from import_export import resources, fields
from django.contrib.admin.models import LogEntry

# Create your models here.

class UserProfile(models.Model):
    #This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    #The addition attributes to include
    website = models.URLField(blank=True)

    #Override the __unicode__() modthod to return what we want
    def __unicode__(self):
        return self.user

class Zone(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "AD Zone"
        verbose_name_plural = "AD Zones"
        
    def __unicode__(self):
        return self.name

class Frame(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    class meta:
        verbose_name = "Frame"
        verbose_name_plural = "Frames"

    def __unicode__(self):
        return self.name

class Stack(models.Model):
    name = models.CharField(max_length=15, blank=True, null=True)

    class meta:
        verbose_name = "Stack"
        verbose_name_plural = "Stacks"

    def __unicode__(self):
        return self.name

class AIXServer(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    owner = models.CharField(max_length=50, blank=True, null=True, default='None')
    frame = models.ForeignKey(Frame)   
    active = models.NullBooleanField(default=True, blank=True)
    #exceptions will be servers we don't want to gather data on - manually set
    exception = models.NullBooleanField(default=False, blank=True)
    decommissioned = models.NullBooleanField(default=False, blank=True)
    #need to see what color 'stack' they are in (sts, mts, fts, etc)
    stack = models.ForeignKey(Stack)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True, default='None')
    zone = models.ForeignKey(Zone)
    os = models.CharField(max_length=10, blank=True, null=True, default='None')
    os_level = models.CharField(max_length=20, blank=True, null=True, default='None')
    centrify = models.CharField(max_length=35, blank=True, null=True, default='None')
    aix_ssh = models.CharField(max_length=25, blank=True, null=True, default='None')
    cent_ssh = models.CharField(max_length=25, blank=True, null=True, default='None')
    xcelys = models.CharField(max_length=35, blank=True, null=True, default='None')
    bash = models.CharField(max_length=25, blank=True, null=True, default='None')
    ssl = models.CharField(max_length=20, blank=True, null=True, default='None')
    java = models.CharField(max_length=20, blank=True, null=True, default='None')
    imperva = models.CharField(max_length=15, blank=True, null=True, default='None')
    netbackup = models.CharField(max_length=35, blank=True, null=True, default='None')
    emc_clar = models.CharField(max_length=20, blank=True, null=True, default='None')
    emc_sym = models.CharField(max_length=20, blank=True, null=True, default='None')
    relationship = models.ManyToManyField('self',
        through='Relationships',
        symmetrical=False,
        related_name='related_to')
    def get_history(self):
        return LogEntry.objects.filter(object_repr=self.name)


    class Meta:
        verbose_name = "AIX Server"
        verbose_name_plural = "AIX Servers"
        ordering = ["name"]


    def __unicode__(self):
        return '%s' % (self.name)

#This will define relationships between LPARs and WPARs and it will probably break EVERYTHING
class Relationships(models.Model):
    parent_lpar = models.ForeignKey(AIXServer, related_name='parent_lpars')
    child_wpar = models.ForeignKey(AIXServer, related_name='child_wpars')

    def __unicode__(self):
            return '%s - %s' % (self.parent_lpar, self.child_wpar)

    class Meta:
        verbose_name = "AIX LPAR-WPAR Relationships"
        verbose_name_plural = "AIX LPAR-WPAR Relationships"


#Meta model to split off the AIX applications in the admin
class AIXApplications(AIXServer):
    class Meta:
        proxy=True
        verbose_name = "AIX Applications"
        verbose_name_plural = "AIX Applications"

class DecommissionedAIXServer(AIXServer):
    class Meta:
        proxy=True
        verbose_name = "AIX Decommissioned Server"
        verbose_name_plural = "AIX Decommissioned Servers"

#Meta model for exporting what you see into Excel and other formats
class AIXServerResource(resources.ModelResource):

    class Meta:
        model = AIXServer
        #fields = ('name', 'owner', 'stack', 'stack', 'frame', 'zone', 'active','exception', 'modified', 'os', 'os_level', 'emc_clar', 'emc_sym')

#Meta model of AIX Server to just show VIO servers
class VIOServer(AIXServer):
    class Meta:
        proxy=True
        verbose_name = "VIO Server"
        verbose_name_plural = "VIO Servers"

class AIXLog(AIXServer):
    class Meta:
        proxy=True
        verbose_name = "AIX Log"
        verbose_name_plural = "AIX Logs"


#Model for AIX error reports
class Errpt(models.Model):
    name = models.ForeignKey(AIXServer)
    report = models.TextField(blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = "AIX Errpt"
        verbose_name_plural = "AIX Errpts"

    def __unicode__(self):
        return unicode(self.name)

class AIXMksysb(models.Model):
    name = models.ForeignKey(AIXServer)
    date = models.DateField("Date", default=datetime.date.today)
    exists = models.NullBooleanField(default=False)
    duplicates = models.NullBooleanField(default=False)

    class Meta:
        verbose_name = "AIX Mksysb"
        verbose_name_plural = "AIX Mksysb"

    def __unicode__(self):
        return unicode(self.name)
    

#Poorly thought out model that only contains storage for AIX servers. Sigh.
class Storage(models.Model):
    name = models.ForeignKey(AIXServer)
    size = models.IntegerField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = "Storage"
        verbose_name_plural = "Storage"
    
    def __unicode__(self):
        return unicode(self.name)

class Power7Inventory(models.Model):
    name = models.ForeignKey(AIXServer)
    lpar_id = models.IntegerField(blank=True, null=True)
    curr_shared_proc_pool_id = models.IntegerField(max_length=4, blank=True, null=True)
    curr_shared_proc_pool_name = models.CharField(max_length=20, blank=True, null=True)
    curr_proc_mode = models.CharField(max_length=20, blank=True, null=True)
    curr_min_proc_units = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    curr_proc_units = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    curr_max_proc_units = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    curr_min_procs = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    curr_procs = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    curr_max_procs = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    curr_sharing_mode = models.CharField(max_length=20, blank=True, null=True)
    curr_uncap_weight = models.IntegerField(max_length=6, blank=True, null=True)
    pend_shared_proc_pool_id = models.IntegerField(max_length=6, blank=True, null=True)
    pend_shared_proc_pool_name = models.CharField(max_length=20, blank=True, null=True)
    pend_proc_mode = models.CharField(max_length=20, blank=True, null=True)
    pend_min_proc_units = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    pend_proc_units = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    pend_max_proc_units = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    pend_min_procs = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    pend_procs = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    pend_max_procs = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    pend_max_procs = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    pend_sharing_mode = models.CharField(max_length=20, blank=True, null=True)
    pend_uncap_weight = models.IntegerField(max_length=6, blank=True, null=True)
    run_proc_units = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    run_procs = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    run_uncap_weight = models.IntegerField(max_length=6, blank=True, null=True)

    curr_min_mem = models.IntegerField(max_length=10, blank=True, null=True)
    curr_mem = models.IntegerField(max_length=10, blank=True, null=True)
    curr_max_mem = models.IntegerField(max_length=10, blank=True, null=True)
    pend_min_mem = models.IntegerField(max_length=10, blank=True, null=True)
    pend_mem = models.IntegerField(max_length=10, blank=True, null=True)
    pend_max_mem = models.IntegerField(max_length=10, blank=True, null=True)
    run_min_mem = models.IntegerField(max_length=10, blank=True, null=True)
    run_mem = models.IntegerField(max_length=10, blank=True, null=True)
    curr_min_num_huge_pages = models.IntegerField(max_length=10, blank=True, null=True)
    curr_num_huge_pages = models.IntegerField(max_length=10, blank=True, null=True)
    pend_mem_expansion = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    curr_mem_expansion = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)

    curr_max_num_huge_pages = models.IntegerField(max_length=10, blank=True, null=True)
    pend_min_num_huge_pages = models.IntegerField(max_length=10, blank=True, null=True)
    pend_num_huge_pages = models.IntegerField(max_length=10, blank=True, null=True)
    pend_max_num_huge_pages = models.IntegerField(max_length=10, blank=True, null=True)
    run_num_huge_pages = models.IntegerField(max_length=10, blank=True, null=True)
    mem_mode = models.CharField(max_length=20, blank=True, null=True)
    desired_hardware_mem_encryption = models.IntegerField(max_length=10, blank=True, null=True)
    curr_hardware_mem_encryption = models.IntegerField(max_length=10, blank=True, null=True)
    curr_hpt_ratio = models.CharField(max_length=10, blank=True, null=True)
    curr_bsr_arrays = models.IntegerField(max_length=10, blank=True, null=True)


    class Meta:
        verbose_name = "Power7 Inventory"
        verbose_name_plural = "Power7 Inventory"

    def __unicode__(self):
        return unicode(self.name)

#Meta model to use for exporting into Excel and other formats
class Power7InventoryResource(resources.ModelResource):
    class Meta:
        model = Power7Inventory




def get_default_zone():
    return Zone.objects.get(id=3)

class LinuxServer(models.Model):
    name = models.CharField(max_length=40, unique=True)
    owner = models.CharField(max_length=30, blank=True, null=True, default='None')
    vmware_cluster = models.CharField(max_length=40, blank=True, null= True) 
    adapter = models.CharField(max_length=20, blank=True, null=True, default='None')
    #active will let us keep historical data of past servers if needed
    active = models.NullBooleanField(default=True, blank=True)

    #exceptions will be servers we don't want to gather data on - manually set
    exception = models.NullBooleanField(default=False, blank=True)
    decommissioned = models.NullBooleanField(default=False, blank=True)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    #last_updated should be auto set by the scripts anytime it is CHANGED
    #this means the script will need to compare values and if something is changed
    #it should change this and add both to the log
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    #I'm not sure why we might need the IP but whatever, just in case..
    ip_address = models.GenericIPAddressField(blank=True, null=True, default='None')
    zone = models.ForeignKey(Zone)
    os = models.CharField(max_length=50, blank=True, null=True, default='None')
    os_level = models.CharField(max_length=20, blank=True, null=True, default='None')
    memory = models.IntegerField(max_length=10, blank=True, null=True)
    cpu = models.IntegerField(max_length=3, blank=True, null=True)
    storage = models.IntegerField(max_length=10, blank=True, null=True)
    centrify = models.CharField(max_length=35, blank=True, null=True, default='None')
    xcelys = models.CharField(max_length=35, blank=True, null=True, default='None')
    bash = models.CharField(max_length=25, blank=True, null=True, default='None')
    ssl = models.CharField(max_length=20, blank=True, null=True, default='None')
    java = models.CharField(max_length=20, blank=True, null=True, default='None')
    imperva = models.CharField(max_length=15, blank=True, null=True, default='None')
    netbackup = models.CharField(max_length=40, blank=True, null=True, default='None')
    log = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Linux Server"
        verbose_name_plural = "Linux Servers"
        ordering = ["name"]

    def __unicode__(self):
        return '%s' % (self.name)

class DecommissionedLinuxServer(LinuxServer):
    class Meta:
        proxy=True
        verbose_name = "Linux Decommissioned Server"
        verbose_name_plural = "Linux Decommissioned Servers"

#Meta model to just show the application versions
class LinuxApplications(LinuxServer):
    class Meta:
        proxy=True
        verbose_name = "Linux Applications"
        verbose_name_plural = "Linux Applications"

#Meta model to use for exporting into Excel and other formats
class LinuxServerResource(resources.ModelResource):
    class Meta:
        model = LinuxServer



#class CapacityPlanning(models.Model):
#    name = models.ForeignKey(AIXServer, related_name='capacity_name')
#    os = models.ForeignKey(AIXServer, related_name='capacity_os')
#    ip_address = models.ForeignKey(AIXServer, related_name='capacity_ip_address')
#    curr_procs = models.ForeignKey(Power7Inventory, related_name = 'capacity_curr_procs')
#    curr_mem = models.ForeignKey(Power7Inventory, related_name = 'capacity_curr_mem')
#    storage = models.IntegerField(max_length=10, blank=True, null=True)
#    database_name = models.CharField(max_length=40, blank=True, null=True)
#
#    class Meta:
#        verbose_name = "Capacity Planning"
#        verbose_name_plural = "Capacity Planning"
#
#    def __unicode__(self):
#        return unicode(self.capacity_name)

#    def save(self, *args, **kwargs):
#        '''On save, update timestamps'''
#        if not self.id:
#            self.created = datetime.datetime.today()
#        self.modified = datetime.datetime.today()
#        return super(Server, self).save(*args, **kwargs)



