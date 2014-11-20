#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to get AIX errpts
#
# Boomer Rehfield - 9/5/2014
#
#########################################################################

import os
from ssh import SSHClient
from django.utils import timezone
from django.contrib.admin.models import LogEntry
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer, Errpt
import test_server
django.setup()



def update_server():
    #right now we are just getting these for the VIO servers
    server_list = AIXServer.objects.filter(name__contains='vio')
    #server_list = AIXServer.objects.filter(name__contains='p1vio01')
    for server in server_list:
        server_is_active=1

        #Make sure the server is set to active and not an exception
        if AIXServer.objects.filter(name=server, active=True, exception=False):
            
            if test_server.ping(server):
                client = SSHClient()
                client.load_system_host_keys()

                #without try, it will break the script if it can't SSH
                try:
                    client.connect(str(server), username="wrehfiel")
                except:
                    print 'SSH to ' + str(server) + ' failed, changing exception'
                    AIXServer.objects.filter(name=server).update(exception=True, modified=timezone.now())

                    #LogEntry.objects.create(action_time='2014-08-25 20:00:00', user_id=11, content_type_id=9, object_id =264, object_repr=server, action
                    LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='SSH failed, changed exception.')
                    server_is_active=0

                if server_is_active:
                    stdin, stdout, stderr = client.exec_command('errpt | tail -n 20"')
                    report = ''

                    #we have to do errpt differently due to the way it is handled by stdout
                    for line in stdout:
                        report = report + str(line)
                    if report == '':
                        report = "The errpt was empty."
                  
                    #let's get the PK for the server
                    server_name = AIXServer.objects.get(name=server)
                    #we don't care about the old record and we'll just overwrite it
                    Errpt.objects.get_or_create(name=server, report=report, modified=timezone.now())
                    change_message = 'Updated errpt.'
                    LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)




#start execution
if __name__ == '__main__':
    print "Getting Errpts..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    from server.models import AIXServer
    update_server()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
