#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve Xcelys versions and drop them into Django dashboard
#
# Boomer Rehfield - 8/7/2014
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
import ping_server
django.setup()


def update_server():
    server_list = AIXServer.objects.all()
    #FIXME quick way of testing a few servers
    #do not use a list/dict as it needs the actual object for the 'server'
    #server_list = AIXServer.objects.filter(name='u3midcap2')
    for server in server_list:
        server_is_active=1
        if AIXServer.objects.filter(name=server, active=True, exception=False):
            #The server looks good, so we're going to ping it to see if it's status has changed
            response = ping_server.ping(server)
            if response == 0:
                AIXServer.objects.filter(name=server).update(active=True)
                client = SSHClient()
                client.load_system_host_keys()
                print server
                try:
                    client.connect(str(server), username="wrehfiel")
                except:
                    print 'SSH to ' + str(server) + ' failed, changing exception'
                    #SSH fails so we set it to an exception, update the modified time, and add a log entry
                    AIXServer.objects.filter(name=server).update(exception=True, modified=timezone.now())
                    LogEntry.objects.create(action_time='2014-08-25 20:00:00', user_id=11, content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='SSH failed, changed exception.')

                    server_is_active=0

                if server_is_active: 
                    stdin, stdout, stderr = client.exec_command('[ -f /opt/xcelys/version ] && cat /opt/xcelys/version || echo "None"')
                    temp_xcelys_version = stdout.readlines()[0]

                    #need to cut the string down
                    xcelys_version = temp_xcelys_version[36:-16]
                    print xcelys_version
                     
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
            else:
                #server is labeled as good, but didn't respond to a ping so we'll change it's status
                AIXServer.objects.filter(name=server).update(active=False)
                print str(server) + ' not responding to ping, setting to inactive.'
                LogEntry.objects.create(action_time='2014-08-25 20:00:00', user_id=11, content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='Ping failed, changed to inactive.')

                




#start execution
if __name__ == '__main__':
    print "Checking Xcelys versions..."
    print timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    print timezone.now()
