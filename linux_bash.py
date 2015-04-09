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
django.setup()


def update_server():

    server_list = LinuxServer.objects.filter(decommissioned=False)

    counter = 0

    for server in server_list:
        #counter += 1
        #print str(counter) + ' - ' + str(server)
        print server.name
        if utilities.ping(server):

            client = SSHClient()
            if utilities.ssh(server, client):
                print server.name
                command = 'rpm -qa | grep bash |grep -v doc'
                stdin, stdout, stderr = client.exec_command(command)
                bash_version = stdout.readlines()[0].rstrip()
                
                bash_version = re.sub(r'x86_64', '', bash_version)
                print bash_version
                print timezone.now()
                #check existing value, if it exists, don't update
                if str(bash_version) != str(server.bash):
                    utilities.log_change(str(server), 'bash', str(server.bash), str(bash_version))
                    LinuxServer.objects.filter(name=server, exception=False, active=True).update(bash=bash_version, modified=timezone.now())



#start execution
if __name__ == '__main__':
    print "Checking Bash versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

