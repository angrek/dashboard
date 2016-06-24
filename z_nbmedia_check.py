#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to check nbmedia server list to see if they are all there
#
# Boomer Rehfield - 4/1/2015
#
#########################################################################

import os
import paramiko

# these are need in django 1.7 and needed vs the django settings command
import django
from django.utils import timezone

from server.models import LinuxServer
import utilities

django.setup()


def update_server():

    server_list = LinuxServer.objects.filter(decommissioned=False, active=True, zone=2)[:20]

    for server in server_list:

        if utilities.ping(server):

            client = paramiko.SSHClient()

            if utilities.ssh(server, client):

                command = 'cat /usr/openv/netbackup/bp.conf'
                stdin, stdout, stderr = client.exec_command(command)

                output = stdout.readlines()
                print '-----------------------'
                print server.name
                for line in output:
                    print line.rstrip()


if __name__ == '__main__':
    print "Checking bp.conf entries..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
