#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve AIX OS levels
#
# Boomer Rehfield - 8/7/2014
#
#########################################################################

import os
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer
import utilities
django.setup()


def update_server():

    server_list = AIXServer.objects.filter(decommissioned=False).exclude(name__contains='vio')

    for server in server_list:
        
        if utilities.ping(server):

            client = SSHClient()
            if utilities.ssh(server, client):
                print server.name
                #with the vio servers we want the ios.level rather than the os_level
                command = 'dzdo emgr -l | grep lquerylv'
                stdin, stdout, stderr = client.exec_command(command)
                if stdout.readlines():
                    print "yes"
                    if server.ifix == False:
                        utilities.log_change(server, 'ifix', 'False', 'True')
                        AIXServer.objects.filter(name=server).update(ifix=True, modified=timezone.now())
                else:
                    print "no"
                    if server.ifix == True:
                        utilities.log_change(server, 'ifix', 'True', 'False')
                        AIXServer.objects.filter(name=server).update(ifix=False, modified=timezone.now())
                #need rstrip() because there are extra characters at the end

                
                #check existing value, if it exists, don't update
                #if str(oslevel) != str(server.os_level):
                #    utilities.log_change(server, 'oslevel', str(server.os_level), str(oslevel))
                #    AIXServer.objects.filter(name=server, exception=False, active=True).update(os_level=oslevel, modified=timezone.now())



#start execution
if __name__ == '__main__':
    print "Checking OS versions..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
