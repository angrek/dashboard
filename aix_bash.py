#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve bash versions and drop them into Django dashboard
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
import test_server
import dashboard_logging

django.setup()


def update_server():
    #server_list = AIXServer.objects.all()
    #FIXME quick way of testing a few servers
    #server_list = AIXServer.objects.filter(name='qinfipcapp')
    #server_list = AIXServer.objects.filter(name='p1fwadb')
    server_list = AIXServer.objects.filter(name='d1bwadb')
    #server_list = ['d1vio01', 'd1vio01']
    #server_list = AIXServer.objects.filter(name__contains='vio')
    counter = 0
    for server in server_list:
        counter += 1
        print str(counter) + ' - ' + str(server)
        server_is_active=1

        #FIXME The thought here is that I don't care if it's active or an exception, I should be retesting it all anyway....
        #if AIXServer.objects.filter(name=server, active=True, exception=False):
        if AIXServer.objects.filter(name=server):

            if test_server.ping(server):
                
                #test SSH
                client = SSHClient()
                client.load_system_host_keys()

                try:
                    client.connect(str(server), username="wrehfiel")
                except:
                    print 'SSH to ' + str(server) + ' failed, changing exception'
                    AIXServer.objects.filter(name=server).update(exception=True, modified=timezone.now())
                    
                    #LogEntry.objects.create(action_time='2014-08-25 20:00:00', user_id=11, content_type_id=9, object_id =264, object_repr=server, action
                    LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='SSH failed, changed exception.')
                    server_is_active=0 

                if server_is_active:
                    #with the vio servers we want the ios.level rather than the os_level
                    command = 'rpm -qa | grep bash |grep -v doc'
                    stdin, stdout, stderr = client.exec_command(command)
                    bash_version = stdout.readlines()[0].rstrip()

                    #check existing value, if it exists, don't update
                    if str(bash_version) != str(server.bash):
                        AIXServer.objects.filter(name=server, exception=False, active=True).update(bash=bash_version, modified=timezone.now())
                        #pretty user the timestamp is auto created even though the table doesn't reflect it... maybe it's in the model
                        change_message = 'Changed bash version to ' + str(bash_version)
                        LogEntry.objects.create(action_time='2014-08-25 20:00:00', user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)
                        #FIXME - ok, we're going to create the manual log here, haven't worked it all out yet how I want to do it though
                        #We can do that or we can FK to the admin log...should we try to add our own columns?
                        #log = AIXServer.objects.log(name=server 



#start execution
if __name__ == '__main__':
    print "Checking Bash versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

