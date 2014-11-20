#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve Linux imperva versions and drop them into Django dashboard
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
from server.models import LinuxServer
import test_server
django.setup()
import re


def update_server():
    server_list = LinuxServer.objects.all()
    #FIXME quick way of testing a few servers
    #server_list = LinuxServer.objects.filter(name='d1bwadb')
    #server_list = LinuxServer.objects.filter(name__contains='db')
    counter = 0
    for server in server_list:
        counter += 1
        print str(counter) + ' - ' + str(server)
        server_is_active=1

        if LinuxServer.objects.filter(name=server):

            if test_server.ping(server, client):

                client = SSHClient()
                if test_server.ssh(server):

                    command = 'lslpp -L | grep -i imper'
                    stdin, stdout, stderr = client.exec_command(command)
                    test = stdout.readlines()

                    try:
                        output = test[0].rstrip()
                        imperva_version = ' '.join(output.split())
                        imperva_version = imperva_version.split(" ")[1].rstrip()

                        #check existing value, if it exists, don't update
                        if str(imperva_version) != str(server.imperva):
                            LinuxServer.objects.filter(name=server).update(imperva=imperva_version, modified=timezone.now())
                            change_message = 'Changed imperva version to ' + str(imperva_version)
                            LogEntry.objects.create(action_time='2014-08-25 20:00:00', user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)
                    except:
                        imperva_version = 'Not installed'
                        if str(imperva_version) != str(server.imperva):
                            LinuxServer.objects.filter(name=server).update(imperva=imperva_version, modified=timezone.now())
                            #pretty user the timestamp is auto created even though the table doesn't reflect it... maybe it's in the model
                            change_message = 'Changed imperva version to ' + str(imperva_version)
                            LogEntry.objects.create(action_time='2014-08-25 20:00:00', user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)



#start execution
if __name__ == '__main__':
    print "Checking Imperva versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

