#!/home/wrehfiel/ENV/bin/python2.7
####################################################
#
# Script to take care of a log of the logging for the
# Django Dashboard. -Boomer Rehfield 11/19/2014
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
from server.models import AIXServer
import ping_server
django.setup()


def failed_ping(server, os):
        if server.active == True:
            AIXServer.objects.filter(name=server).update(active=False, modified=timezone.now())
            LogEntry.objects.create(action_time=timezone.now(), user_id=11 ,content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='Ping failed, changed to inactive.')


        t = LinuxServer.objects.get(name=server)
        if t.active == True:
            LinuxServer.objects.filter(name=server).update(active=False, modified=timezone.now())
            print str(server) + ' not responding to ping, setting to inactive.'
            #FIXME I need a check here otherwise it isn't really a change, it's updating the same value
            LogEntry.objects.create(action_time=timezone.now(), user_id=11 ,content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='Ping failed, changed to inactive.')





def ping(server, os):
    response = os.system("ping -c 1 " + str(server) + "> /dev/null 2>&1")

    return response

#ping(server)










