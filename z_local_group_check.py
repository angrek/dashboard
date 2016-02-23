#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to search for local groups with 500 id
#
# Boomer Rehfield - 2/8/2016
#
#########################################################################

import os, re
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import LinuxServer
import utilities
import paramiko
django.setup()


def update_server():

    server_list = LinuxServer.objects.filter(decommissioned=False)

    counter = 0

    print '-------------------' 
    for server in server_list:
        #counter += 1
        #print str(counter) + ' - ' + server
        if utilities.ping(server):

            client = paramiko.SSHClient()
            if utilities.ssh(server, client):
                command = "dzdo grep :501: /etc/group"
                stdin, stdout, stderr = client.exec_command(command)
                try:
                    bash_version = stdout.readlines()[0].rstrip()
                except:
                    continue
               
                print server.name + " ->      " + bash_version.rstrip()
                #print bash_version.rstrip()
                #print line.rstrip()
                    #print timezone.now()
                #check existing value, if it exists, don't update
                #if str(bash_version) != str(server.bash):
                    #utilities.log_change(server, 'bash', str(server.bash), str(bash_version))
                    #LinuxServer.objects.filter(name=server, exception=False, active=True).update(bash=bash_version, modified=timezone.now())



#start execution
if __name__ == '__main__':
    print "Checking for groups with the 500 id...."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

