#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve OS levels and drop them into Django dashboard
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
from server.models import Server
django.setup()


def update_server():
    #server_list = Server.objects.all()
    #FIXME quick way of testing a few servers
    #server_list = Server.objects.filter(name='d2vio01')
    #server_list = ['d1vio01', 'd1vio01']
    server_list = Server.objects.filter(name__contains='vio')
    for server in server_list:
        print server
        if Server.objects.filter(name=server, active=True, exception=False):
            client = SSHClient()
            client.load_system_host_keys()
            client.connect(str(server), username="wrehfiel")
            command = 'oslevel -s'
            stdin, stdout, stderr = client.exec_command(command)
            oslevel = stdout.readlines()[0]

            #check existing value, if it exists, don't update
            if str(oslevel) != str(server.os_level):
                Server.objects.filter(name=server, exception=False, active=True).update(os_level=oslevel)
                Server.objects.filter(name=server, exception=False, active=True).update(modified=timezone.now())
                #pretty user the timestamp is auto created even though the table doesn't reflect it... maybe it's in the model
                change_message = 'Changed os_level to ' + str(oslevel)
                LogEntry.objects.create(action_time='2014-08-25 20:00:00', user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)
                #FIXME - ok, we're going to create the manual log here, haven't worked it all out yet how I want to do it though
                #We can do that or we can FK to the admin log...should we try to add our own columns?
                #log = Server.objects.log(name=server 




#start execution
if __name__ == '__main__':
    print "Checking OS versions..."
    print timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    print timezone.now()
