#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to check servers for a specific user on all servers
#
# Boomer Rehfield - 8/7/2014
#
#########################################################################

import os
from paramiko import SSHClient

# these are need in django 1.7 and needed vs the django settings command
from django.utils import timezone
import django

from server.models import LinuxServer
import utilities

django.setup()


def update_server():

    server_count = 0
    server_list = LinuxServer.objects.filter(decommissioned=False)

    for server in server_list:

        if utilities.ping(server):

            client = SSHClient()
            if utilities.ssh(server, client):
                command = 'adquery user | grep ctesta'
                stdin, stdout, stderr = client.exec_command(command)
                try:
                    exists = stdout.readlines()[0].rstrip()
                    print '--------------------'
                    print server.name
                    print exists
                    server_count = server_count + 1
                    command2 = 'ls -l /home | grep ctesta'
                    stdin, stdout, stderr = client.exec_command(command2)
                    try:
                        exists2 = stdout.readlines()[0].rstrip()
                        print exists2
                    except:
                        print 'No home directory'

                except:
                    continue
    print "Total number of Linux servers: " + str(server_count)


if __name__ == '__main__':
    print "Checking for username ctesta on all Linux servers."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
