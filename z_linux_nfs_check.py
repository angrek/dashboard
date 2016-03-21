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
            command = 'dzdo cat /etc/fstab | grep nfs | grep -v netdev | grep -v "#"'
            stdin, stdout, stderr = client.exec_command(command)
            lines = stdout.readlines()
            for line in lines:
                print server.name + ' - ' + line
            


#start execution
if __name__ == '__main__':
    print "Checking Bash versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = LinuxServer.objects.filter(decommissioned=False, active=True, zone=1)

    pool = Pool(40)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

