#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve Linux SSL versions on the servers and drop them into Django dashboard
#
# Boomer Rehfield - 11/13/2014
#
#########################################################################

import os
import re
from ssh import SSHClient
import paramiko
from django.utils import timezone

#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
import ping_server
django.setup()


def update_server():
    counter = 0
    server_list = LinuxServer.objects.all()
    for server in server_list:
        server_is_active = 1

        if LinuxServer.objects.filter(name=server, active=True, exception=False):
            
            response = ping_server.ping(server)
            #ping test
            if response == 0:
                client = SSHClient()
                client.load_system_host_keys()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    client.connect(str(server), username="wrehfiel")
                except:
                    #FIXME - need to check and see if it was an exception before and make it one if it wasn't
                    continue

                stdin, stdout, stderr = client.exec_command('rpm -qa | grep openssl | grep -v devel | uniq')
                #this is going to pull 4 different parts of ssl, we just need the base
                rows = stdout.readlines()
                ssl = str(rows[0])

                #cutton off the beginning and end, not really needed.
                ssl = re.sub('openssl-', '', ssl)
                ssl = re.sub('.x86_64', '', ssl)

                #if existing value is the same, don't update
                if str(ssl) != str(server.ssl):
                    LinuxServer.objects.filter(name=server, exception=False, active=True).update(ssl=ssl, modified=timezone.now())
            else:
                LinuxServer.objects.filter(name=server).update(active=False, modified=timezone.now())
                #print str(server) + ' not responding to ping, setting to inactive.'
                LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='Ping failed, changed to inactive.')




#start execution
if __name__ == '__main__':
    print "Checking SSL versions..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    from server.models import LinuxServer
    update_server()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
