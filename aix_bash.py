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
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer
import test_server
import dashboard_logging

django.setup()


def update_server():
    server_list = AIXServer.objects.filter(decommissioned=False)
    #server_list = AIXServer.objects.filter(name='dltsodsdb')
    #server_list = AIXServer.objects.filter(name__contains='vio')

    counter = 0
    for server in server_list:

        if test_server.ping(server):
            
            client = SSHClient()
            if test_server.ssh(server, client):

                command = 'rpm -qa | grep bash |grep -v doc'
                stdin, stdout, stderr = client.exec_command(command)
                bash_version = stdout.readlines()[0].rstrip()

                #check existing value, if it exists, don't update
                if str(bash_version) != str(server.bash):
                    dashboard_logging.log_change(str(server), 'bash', str(server.bash), str(bash_version))

                    AIXServer.objects.filter(name=server).update(bash=bash_version, modified=timezone.now())



#start execution
if __name__ == '__main__':
    print "Checking Bash versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

