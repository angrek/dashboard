from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class UserProfile(models.Model):
    #This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    #The addition attributes to include
    website = models.URLField(blank=True)

    #Override the __unicode__() modthod to return what we want
    def __unicode__(self):
        return self.user



class Server(models.Model):
    name = models.CharField(max_length=30)
    
    #active will let us keep historical data of past servers if needed
    active = models.NullBooleanField(default=True, blank=True)

    #exceptions will be servers we don't want to gather data on - manually set
    exception = models.NullBooleanField(default=False, blank=True)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    #last_updated should be auto set by the scripts anytime it is CHANGED
    #this means the script will need to compare values and if something is changed
    #it should change this and add both to the log
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    #I'm not sure why we might need the IP but whatever, just in case..
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    os = models.CharField(max_length=10, blank=True, null=True)
    os_level = models.CharField(max_length=20, blank=True, null=True)
    centrify = models.CharField(max_length=35, blank=True, null=True)
    xcelys = models.CharField(max_length=35, blank=True, null=True)
    ssl = models.CharField(max_length=20, blank=True, null=True)
    java = models.CharField(max_length=20, blank=True, null=True)
    log = models.TextField(blank=True, null=True)


    def __unicode__(self):
        return self.name


#    def save(self, *args, **kwargs):
#        '''On save, update timestamps'''
#        if not self.id:
#            self.created = datetime.datetime.today()
#        self.modified = datetime.datetime.today()
#        return super(Server, self).save(*args, **kwargs)


