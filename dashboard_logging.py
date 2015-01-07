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
django.setup()


def log_change(server, app, old_version, new_version):
    change_message = 'Changed ' + app + ' from ' + old_version + ' to ' + new_version
    LogEntry.objects.create(action_time='2014-08-25 20:00:00', user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2,
 change_message=change_message)













