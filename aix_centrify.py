#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to get centrify version and drop it into Django dashboard
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
import ping_server
django.setup()



def update_server():
    #server_list = Server.objects.all()
    #just a quick way to on off test a server without the whole list
    server_list = Server.objects.filter(name='t3dbatest')
    for server in server_list:
        server_is_active=1

        #these are hardcoded because
        #none of the vio servers have Centrify installed on them
        server_exceptions = ['d1vio01', 'd1vio02', 'd2vio01', 'd2vio02', 'p1vio01', 'p1vio02', 'p3vio01', 'p3vio02', 'p1sasvio01', 'p1sasvio02', 'p720vio01', 'p720vio02']

        #Make sure the server is set to active and not an exception
        if Server.objects.filter(name=server, active=True, exception=False) and str(server) not in server_exceptions:
            response = ping_server.ping(server)
            
            #typically = is false, but that's what ping gives back for a positive
            if response == 0:
                client = SSHClient()
                client.load_system_host_keys()

                #without try, it will break the script if it can't SSH
                try:
                    client.connect(str(server), username="wrehfiel")
                except:
                    print 'SSH to ' + str(server) + ' failed, changing exception'
                    Server.objects.filter(name=server).update(exception=True)
                    Server.objects.filter(name=server).update(modified=timezone.now())

                    #LogEntry.objects.create(action_time='2014-08-25 20:00:00', user_id=11, content_type_id=9, object_id =264, object_repr=server, action
                    LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='SSH failed, changed exception.')
                    server_is_active=0

                if server_is_active:
                    stdin, stdout, stderr = client.exec_command('adinfo -v')
                    centrify = stdout.readlines()[0]
                    #strings in Python are immutable so we need to create a new one
                    new_centrify = centrify[8:-2]
                   
                    #if it's the same version, we don't need to update the record
                    if str(new_centrify) != str(server.centrify):
                        old_version = str(server.centrify)
                        Server.objects.filter(name=server, exception=False, active=True).update(centrify=new_centrify)
                        Server.objects.filter(name=server, exception=False, active=True).update(modified=timezone.now())
                        change_message = 'Changed Centrify version from ' + old_version + ' to ' + str(new_centrify) + '.' 
                        LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)
            else:
                Server.objects.filter(name=server).update(active=False)
                print str(server) + ' not responding to ping, setting to inactive.'
                Server.objects.filter(name=server, exception=False, active=True).update(modified=timezone.now())
                LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='Ping failed, changed to inactive.')




#start execution
if __name__ == '__main__':
    print "Checking centrify version..."
    print timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    from server.models import Server
    update_server()
    print timezone.now()
