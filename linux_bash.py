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
from multiprocessing import Pool
django.setup()


def update_server(server):

        
    if utilities.ping(server):

        client = paramiko.SSHClient()
        if utilities.ssh(server, client):
            print server.name
            command = 'dzdo rpm -qa | grep bash |grep -v doc| grep -v completion'
            stdin, stdout, stderr = client.exec_command(command)
            bash_version = stdout.readlines()[0].rstrip()
            
            bash_version = re.sub(r'.x86_64', '', bash_version)
            bash_version = re.sub(r'bash-', '', bash_version)
            print bash_version
            
            #check existing value, if it exists, don't update
            if str(bash_version) != str(server.bash):
                utilities.log_change(server, 'bash', str(server.bash), str(bash_version))
                LinuxServer.objects.filter(name=server, exception=False, active=True).update(bash=bash_version, modified=timezone.now())



#start execution
if __name__ == '__main__':
    print "Checking Bash versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = LinuxServer.objects.filter(decommissioned=False)

    pool = Pool(30)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

