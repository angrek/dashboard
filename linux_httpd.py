#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve bash versions and drop them into Django dashboard
#
# Boomer Rehfield - 11/13/2014
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

    for server in server_list:
        #counter += 1
        #print str(counter) + ' - ' + server
        if utilities.ping(server):

            client = paramiko.SSHClient()
            if utilities.ssh(server, client):
                flag = 0
                command = 'ps -ef | grep httpd | grep -v grep | uniq'
                stdin, stdout, stderr = client.exec_command(command)
                for line in stdout.readlines():
                    if line: 
                        flag = 1

                if flag == 1:
                    print "--------------------------"
                    print server.name
                    print "Apache is running"
                    print line.rstrip()
                    command2 = 'rpm -qa | grep httpd | grep -v devel | grep -v tools | grep -v manual'
                    stdin, stdout, stderr = client.exec_command(command2)
                    for line2 in stdout.readlines():
                        if line2: 
                            print line2.rstrip()

    print "-----------------------"
                #check existing value, if it exists, don't update
                #if str(bash_version) != str(server.bash):
                #    utilities.log_change(server, 'bash', str(server.bash), str(bash_version))
                #    LinuxServer.objects.filter(name=server, exception=False, active=True).update(bash=bash_version, modified=timezone.now())



#start execution
if __name__ == '__main__':
    print "Checking Bash versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

