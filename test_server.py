#!/home/wrehfiel/ENV/bin/python2.7
####################################################
#
# Script to ping the servers to see if they are up.
# If they are not, then set them as inactive in the
# Django Dashboard. -Boomer Rehfield 9/4/2014
#
####################################################

#server = 'p1rhrep'
import os
from ssh import SSHClient
from django.utils import timezone
from django.contrib.admin.models import LogEntry
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer, LinuxServer
import dashboard_logging

django.setup()

#test ping...  I know, not a very descriptive name...
def ping(server):
    response = os.system("ping -c 1 " + str(server) + "> /dev/null 2>&1")
    if response == 0:
        print "Ping succeeded"

        if server.active == False:
            server.active=True
            server.modified=timezone.now()
            server.save()
            LogEntry.objects.create(action_time=timezone.now(), user_id=11 ,content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='Ping succeeded, changed to active.')
    else:
        print "Ping failed"
        if server.active == True:
            server.active=False
            server.modified=timezone.now()
            server.save()
            LogEntry.objects.create(action_time=timezone.now(), user_id=11 ,content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='Ping failed, changed to inactive.')

    #for the sake of brevetiy elsewhere, I'm flipping this. Returning 0 for a good result is stupid. *cough* Looking at you ping...
    if response == 0:
        response = 1
    else:
        response = 0
    return response


#test ssh... duh
def ssh(server, client):

    client.load_system_host_keys()

    try:
        client.connect(str(server), username="wrehfiel")
        print 'ssh good'
        if server.exception == True:
            server.exception = False
            server.save()
            LogEntry.objects.create(action_time=timezone.now(), user_id=11 ,content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='SSH succeeded, changed exception.')
            print 'changed exception'
        response = 1

    except:
        print 'ssh bad'
        if server.exception == False:
            server.exception = True
            server.save()
            LogEntry.objects.create(action_time=timezone.now(), user_id=11 ,content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='SSH failed, changed exception.')
            print 'changed exception'
        response = 0
    return response










