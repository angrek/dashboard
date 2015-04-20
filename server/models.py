from django.db import models
from django.contrib.auth.models import User
import datetime
from import_export import resources, fields, widgets
from django.contrib.admin.models import LogEntry


class UserProfile(models.Model):
    #This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)
    test = models.CharField(max_length=25, blank=True, null=True)

    def __unicode__(self):
        return self.user

class Zone(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "AD Zone"
        verbose_name_plural = "AD Zones"
        
    def __unicode__(self):
        return self.name

class Java(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True, default='None')

    class Meta:
        verbose_name = "Java"
        verbose_name_plural = "Java"

    def __unicode__(self):
        return self.name

class Frame(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    short_name = models.CharField(max_length=15, blank=True, null=True, default='None')
    firmware_version = models.CharField(max_length=15, blank=True, null=True, default='None')


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

class SubStack(models.Model):
    name = models.CharField(max_length=15, blank=True, null=True)

    class meta:
        verbose_name = "Sub Stack"
        verbose_name_plural = "Sub Stacks"

    def __unicode__(self):
        return self.name

SERVER_ENV_CHOICES = (
    (1, 'None'),
    (2, 'DEV'),
    (3, 'UAT'),
    (4, 'QA'),
    (5, 'PROD-INFRA'),
    (6, 'PREPROD'),
    (7, 'PROD'),
    (8, 'DR/COB'),
)

class AIXServer(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    owner = models.CharField(max_length=50, blank=True, null=True, default='None')
    frame = models.ForeignKey(Frame)   
    active = models.NullBooleanField(default=True, blank=True)
    exception = models.NullBooleanField(default=False, blank=True)
    decommissioned = models.NullBooleanField(default=False, blank=True)
    stack = models.ForeignKey(Stack)
    substack = models.ForeignKey(SubStack, default=1)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True, default='None')
    zone = models.ForeignKey(Zone)
    os = models.CharField(max_length=10, blank=True, null=True, default='None')
    os_level = models.CharField(max_length=20, blank=True, null=True, default='None')
    asm = models.NullBooleanField(default=False, blank=True)
    ifix = models.NullBooleanField(default=False, blank=True)
    tmef = models.FloatField(default=0.00)
    powerha = models.CharField(max_length=20, blank=True, null=True, default='None')
    centrify = models.CharField(max_length=35, blank=True, null=True, default='None')
    aix_ssh = models.CharField(max_length=25, blank=True, null=True, default='None')
    cent_ssh = models.CharField(max_length=25, blank=True, null=True, default='None')
    xcelys = models.CharField(max_length=35, blank=True, null=True, default='None')
    bash = models.CharField(max_length=35, blank=True, null=True, default='None')
    ssl = models.CharField(max_length=45, blank=True, null=True, default='None')
    imperva = models.CharField(max_length=25, blank=True, null=True, default='None')
    netbackup = models.CharField(max_length=35, blank=True, null=True, default='None')
    rsyslog = models.CharField(max_length=30, blank=True, null=True, default='None')
    samba = models.CharField(max_length=35, blank=True, null=True, default='None')
    java = models.ManyToManyField(Java, default='None')

    emc_clar = models.CharField(max_length=20, blank=True, null=True, default='None')
    emc_sym = models.CharField(max_length=20, blank=True, null=True, default='None')
    server_env = models.NullBooleanField(default=False, blank=True)
    server_env_marker = models.IntegerField(choices=SERVER_ENV_CHOICES, default=1)
    server_env_text = models.TextField(blank=True, null=True)
    curr_lpar_score = models.IntegerField(max_length=3, blank=True, null=True)
    predicted_lpar_score = models.IntegerField(max_length=3, blank=True, null=True)
    application_paths = models.TextField(blank=True, null=True)
    #relationship = models.ManyToManyField('self',
    #    through='Relationships',
    #    symmetrical=False,
    #    related_name='related_to')
    def get_history(self):
        return LogEntry.objects.filter(object_repr=self.name)

    #this is to put an image link in the admin to each server's ganglia page
    def image_tag(self):
        frame_short_name = str(self.frame)[:3] + '-' + str(self.frame)[-5:]
        link = '<a href="http://p795agmon/?r=hour&cs=&ce=&m=cpu_used_report&s=by+name&c=' + frame_short_name + '&h=' + self.name + '.wellcare.com&host_regex=&max_graphs=0&tab=m&vn=&sh=1&z=small&hc=4"><img src="http://p1rhrep/g2.jpg" title="Ganglia Page"></a>'
        return u'%s' % link
    image_tag.short_description = 'G'
    image_tag.allow_tags = True

    class Meta:
        verbose_name = "AIX Server"
        verbose_name_plural = "AIX Servers"
        ordering = ["name"]


    def __unicode__(self):
        return '%s' % (self.name)

class HistoricalAIXData(models.Model):
    date = models.DateField("Date", default=datetime.date.today)
    name = models.ForeignKey(AIXServer)
    frame = models.ForeignKey(Frame)   
    active = models.NullBooleanField(default=True, blank=True)
    exception = models.NullBooleanField(default=False, blank=True)
    decommissioned = models.NullBooleanField(default=False, blank=True)
    created = models.DateTimeField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True, default='None')
    zone = models.ForeignKey(Zone)
    os_level = models.CharField(max_length=20, blank=True, null=True, default='None')
    centrify = models.CharField(max_length=35, blank=True, null=True, default='None')
    aix_ssh = models.CharField(max_length=25, blank=True, null=True, default='None')
    cent_ssh = models.CharField(max_length=25, blank=True, null=True, default='None')
    xcelys = models.CharField(max_length=35, blank=True, null=True, default='None')
    bash = models.CharField(max_length=25, blank=True, null=True, default='None')
    ssl = models.CharField(max_length=40, blank=True, null=True, default='None')
    imperva = models.CharField(max_length=15, blank=True, null=True, default='None')
    netbackup = models.CharField(max_length=35, blank=True, null=True, default='None')
    rsyslog = models.CharField(max_length=30, blank=True, null=True, default='None')
    samba = models.CharField(max_length=35, blank=True, null=True, default='None')
    emc_clar = models.CharField(max_length=20, blank=True, null=True, default='None')
    emc_sym = models.CharField(max_length=20, blank=True, null=True, default='None')

    class Meta:
        verbose_name = "Historical AIX Data"
        verbose_name_plural = "Historical AIX Data"
        ordering = ["-date"]
        unique_together = ("date", "name")


    def __unicode__(self):
        return '%s' % (self.name)



##This will define relationships between LPARs and WPARs and it will probably break EVERYTHING
#class Relationships(models.Model):
#    parent_lpar = models.ForeignKey(AIXServer, related_name='parent_lpars')
#    child_wpar = models.ForeignKey(AIXServer, related_name='child_wpars')
#
#    def __unicode__(self):
#            return '%s - %s' % (self.parent_lpar, self.child_wpar)
#
#    class Meta:
#        verbose_name = "AIX LPAR-WPAR Relationships"
#        verbose_name_plural = "AIX LPAR-WPAR Relationships"


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

class AIXPowerHA(AIXServer):
    class Meta:
        proxy=True
        verbose_name = "AIX PowerHA Systems"
        verbose_name_plural = "AIX PowerHA Systems"

#Meta model for exporting what you see into Excel and other formats
class AIXServerResource(resources.ModelResource):

    class Meta:
        model = AIXServer
        #test = fields.Field(column_name='frame', attribute='frame', widget=ForeignLookupKeyWidget(Frame, 'name'))
        fields = ('name', 'owner', 'frame', 'active', 'exception', 'decommissioned', 'stack', 'created', 'modified', 'ip_address', 'zone', 'os', 'os_level', 'powerha', 'centrify', 'aix_ssh', 'cent_ssh', 'xcelys', 'bash', 'ssl', 'java', 'imperva', 'netbackup', 'emc_clar', 'emc_sym', 'relationship')

#Meta model of AIX Server to just show VIO servers
class VIOServer(AIXServer):
    class Meta:
        proxy=True
        verbose_name = "VIO Server"
        verbose_name_plural = "VIO Servers"

#Meta model of AIX Server (temp) to show Affinity
class AIXAffinity(AIXServer):
    class Meta:
        proxy=True
        verbose_name = "AIX Affinity"
        verbose_name_plural = "AIX Affinity"

class AIXServerENV(AIXServer):
    class Meta:
        proxy=True
        verbose_name = "AIX Server ENV"
        verbose_name_plural = "AIX Sever ENV"

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
        verbose_name = "AIX Storage"
        verbose_name_plural = "AIX Storage"
    
    def __unicode__(self):
        return unicode(self.name)

class Power7Inventory(models.Model):
    name = models.ForeignKey(AIXServer)
    lpar_id = models.IntegerField(blank=True, null=True)
    frame = models.ForeignKey(Frame, blank=True, null=True)   
    active = models.NullBooleanField(default=True, blank=True)
    exception = models.NullBooleanField(default=False, blank=True)
    decommissioned = models.NullBooleanField(verbose_name='Decom', default=False, blank=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)
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
    curr_hardware_mem_expansion = models.IntegerField(max_length=10, blank=True, null=True)
    desired_hardware_mem_expansion = models.IntegerField(max_length=10, blank=True, null=True)
    curr_hpt_ratio = models.CharField(max_length=10, blank=True, null=True)
    curr_bsr_arrays = models.IntegerField(max_length=10, blank=True, null=True)


    class Meta:
        verbose_name = "AIX Power Inventory"
        verbose_name_plural = "AIX Power Inventory"

    def __unicode__(self):
        return unicode(self.name)

#Meta model to use for exporting into Excel and other formats
class Power7InventoryResource(resources.ModelResource):
    class Meta:
        model = Power7Inventory




def get_default_zone():
    return Zone.objects.get(id=3)

class LinuxServer(models.Model):
    name = models.CharField(max_length=40, primary_key=True)
    owner = models.CharField(max_length=30, blank=True, null=True, default='None')
    vmware_cluster = models.CharField(max_length=40, blank=True, null= True) 
    adapter = models.CharField(max_length=20, blank=True, null=True, default='None')
    active = models.NullBooleanField(default=True, blank=True)
    exception = models.NullBooleanField(default=False, blank=True)
    decommissioned = models.NullBooleanField(default=False, blank=True)
    stack = models.ForeignKey(Stack, default=1)
    Substack = models.ForeignKey(SubStack, default=1)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True, default='0.0.0.0')
    zone = models.ForeignKey(Zone)
    os = models.CharField(max_length=50, blank=True, null=True, default='None')
    os_level = models.CharField(max_length=20, blank=True, null=True, default='None')
    memory = models.IntegerField(max_length=10, blank=True, null=True)
    cpu = models.IntegerField(max_length=3, blank=True, null=True)
    storage = models.IntegerField(max_length=10, blank=True, null=True)
    centrify = models.CharField(max_length=35, blank=True, null=True, default='None')
    xcelys = models.CharField(max_length=35, blank=True, null=True, default='None')
    bash = models.CharField(max_length=25, blank=True, null=True, default='None')
    ssl = models.CharField(max_length=40, blank=True, null=True, default='None')
    java = models.CharField(max_length=20, blank=True, null=True, default='None')
    imperva = models.CharField(max_length=15, blank=True, null=True, default='None')
    netbackup = models.CharField(max_length=40, blank=True, null=True, default='None')
    syslog = models.CharField(max_length=30, blank=True, null=True, default='None')
    rsyslog = models.CharField(max_length=30, blank=True, null=True, default='None')
    rsyslog_r = models.NullBooleanField(default=False, blank=True)
    samba = models.CharField(max_length=40, blank=True, null=True, default='None')
    server_env = models.NullBooleanField(default=False, blank=True)
    server_env_marker = models.IntegerField(choices=SERVER_ENV_CHOICES, default=1)
    server_env_text = models.TextField(blank=True, null=True, default='None')
    application_paths = models.TextField(blank=True, null=True, default='None')
    log = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Linux Server"
        verbose_name_plural = "Linux Servers"
        ordering = ["name"]

    def __unicode__(self):
        return '%s' % (self.name)


class HistoricalLinuxData(models.Model):
    date = models.DateField("Date", default=datetime.date.today)
    name = models.ForeignKey(LinuxServer)
    owner = models.CharField(max_length=30, blank=True, null=True, default='None')
    vmware_cluster = models.CharField(max_length=40, blank=True, null= True) 
    adapter = models.CharField(max_length=20, blank=True, null=True, default='None')
    active = models.NullBooleanField(default=True, blank=True)
    exception = models.NullBooleanField(default=False, blank=True)
    decommissioned = models.NullBooleanField(default=False, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
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
    ssl = models.CharField(max_length=40, blank=True, null=True, default='None')
    java = models.CharField(max_length=20, blank=True, null=True, default='None')
    imperva = models.CharField(max_length=15, blank=True, null=True, default='None')
    netbackup = models.CharField(max_length=40, blank=True, null=True, default='None')
    syslog = models.CharField(max_length=30, blank=True, null=True, default='None')
    rsyslog = models.CharField(max_length=30, blank=True, null=True, default='None')
    server_env = models.NullBooleanField(default=False, blank=True)

    class Meta:
        verbose_name = "Historical Linux Data"
        verbose_name_plural = "Historical Linux Data"
        ordering = ["-date"]
        unique_together = ("date", "name")

    def __unicode__(self):
        return '%s' % (self.name)



class DecommissionedLinuxServer(LinuxServer):
    class Meta:
        proxy=True
        verbose_name = "Linux Decommissioned Server"
        verbose_name_plural = "Linux Decommissioned Servers"

##Meta model to just show the application versions
class LinuxApplications(LinuxServer):
    class Meta:
        proxy=True
        verbose_name = "Linux Applications"
        verbose_name_plural = "Linux Applications"

##Meta model to use for exporting into Excel and other formats
class LinuxServerResource(resources.ModelResource):
    class Meta:
        model = LinuxServer

class LinuxServerENV(LinuxServer):
    class Meta:
        proxy=True
        verbose_name = "Linux Server ENV"
        verbose_name_plural = "Linux Sever ENV"

####################### WINDOWS TESTING###################################

class WindowsServer(models.Model):
    name = models.CharField(max_length=40, primary_key=True)
    owner = models.CharField(max_length=30, blank=True, null=True, default='None')
    active = models.NullBooleanField(default=True, blank=True)
    exception = models.NullBooleanField(default=False, blank=True)
    decommissioned = models.NullBooleanField(default=False, blank=True)
    stack = models.ForeignKey(Stack, default=1)
    substack = models.ForeignKey(SubStack, default=1)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)
    vmware_cluster = models.CharField(max_length=40, blank=True, null= True) 
    adapter = models.CharField(max_length=20, blank=True, null=True, default='None')
    ip_address = models.GenericIPAddressField(blank=True, null=True, default='None')
    zone = models.ForeignKey(Zone)
    os = models.CharField(max_length=50, blank=True, null=True, default='None')
    os_level = models.CharField(max_length=20, blank=True, null=True, default='None')
    memory = models.IntegerField(max_length=10, blank=True, null=True)
    cpu = models.IntegerField(max_length=3, blank=True, null=True)
    storage = models.IntegerField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = "Windows Server"
        verbose_name_plural = "Windows Servers"
        ordering = ["name"]

    def __unicode__(self):
        return '%s' % (self.name)

class WindowsServerResource(resources.ModelResource):
    class Meta:
        model = WindowsServer


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



