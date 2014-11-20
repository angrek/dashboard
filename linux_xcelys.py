#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve Linux Xcelys versions and drop them into Django dashboard
#
# Boomer Rehfield - 11/13/2014
#
#########################################################################

import os
from ssh import SSHClient
from django.utils import timezone
from django.contrib.admin.models import LogEntry
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer
import re
import test_server
django.setup()


def update_server():
    server_list = AIXServer.objects.all()
    #FIXME quick way of testing a few servers
    #do not use a list/dict as it needs the actual object for the 'server'
    #server_list = AIXServer.objects.filter(name='u3midcap2')
    for server in server_list:
        server_is_active=1

        if AIXServer.objects.filter(name=server):

            if test_server.ping(server):

                #AIXServer.objects.filter(name=server).update(active=True)
                client = SSHClient()
                client.load_system_host_keys()
                try:
                    client.connect(str(server), username="wrehfiel")
                except:
                    #SSH fails so we set it to an exception, update the modified time, and add a log entry
                    AIXServer.objects.filter(name=server).update(exception=True, modified=timezone.now())
                    LogEntry.objects.create(action_time='2014-08-25 20:00:00', user_id=11, content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='SSH failed, changed exception.')
                    continue


                stdin, stdout, stderr = client.exec_command('[ -f /opt/xcelys/version ] && cat /opt/xcelys/version || echo "None"')
                temp_xcelys_version = stdout.readlines()[0]

                #need to cut the string down
                xcelys_version = temp_xcelys_version[36:-16]
                 
                #check existing value, if it exists, don't update
                if str(xcelys_version) != str(server.xcelys):
                    AIXServer.objects.filter(name=server, exception=False, active=True).update(xcelys=xcelys_version)
                    AIXServer.objects.filter(name=server, exception=False, active=True).update(modified=timezone.now())
                    #pretty sure the timestamp is auto created even though the table doesn't reflect it... maybe it's in the model
                    change_message = 'Changed xcelys to ' + str(xcelys_version)
                    LogEntry.objects.create(action_time='2014-08-25 20:00:00', user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)
                    #FIXME - ok, we're going to create the manual log here, haven't worked it all out yet how I want to do it though
                    #We can do that or we can FK to the admin log...should we try to add our own columns?
                    #log = AIXServer.objects.log(name=server 



#start execution
if __name__ == '__main__':
    print "Checking Xcelys versions..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
