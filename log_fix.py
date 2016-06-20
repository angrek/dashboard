#!/home/wrehfiel/ENV/bin/python2.7
####################################################
#
# Script to fix a missing content type bug that broke stuff
#
#  -Boomer Rehfield 1/15/2016
#
####################################################


# these are need in django 1.7 and needed vs the django settings command
import django
from django.contrib.admin.models import LogEntry

from server.models import AIXServer
from server.models import LinuxServer

django.setup()


log_entries = LogEntry.objects.filter(content_type_id=9)

for entry in log_entries:
    server_type = ''
    print "------------------"
    print entry.id
    print entry.object_repr
    print entry.content_type_id
    print entry.change_message
    print entry.action_time
    new_time = entry.action_time
    print "length"
    print len(entry.object_repr.rstrip())

    try:
        test = AIXServer.objects.get(name=entry.object_repr.rstrip())
        server_type = "AIX"
        print test.os
        if entry.content_type_id == 9:
            print "Changing content_type from 9 to 15"
            entry.content_type_id = 15
            entry.action_time = new_time
            entry.save()

    except:
        test = LinuxServer.objects.get(name=entry.object_repr.rstrip())
        server_type = "Linux"
        print test.os
        if entry.content_type_id == 9:
            print "Changing content_type from 9 to 16"
            entry.content_type_id = 16
            entry.action_time = new_time
            entry.save()
    print server_type
