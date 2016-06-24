#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to check if rsyslog has an old entry
#
# Boomer Rehfield - 8/21/2015
#
#########################################################################

import os
import paramiko

# these are need in django 1.7 and needed vs the django settings command
from django.utils import timezone
import django

from server.models import LinuxServer
import utilities
django.setup()


def update_server():

    server_list = LinuxServer.objects.filter(decommissioned=False)

    for server in server_list:

        if utilities.ping(server):

            client = paramiko.SSHClient()

            if utilities.ssh(server, client):

                command = 'dzdo grep itsec /etc/*syslog*'
                stdin, stdout, stderr = client.exec_command(command)

                try:
                    output = stdout.readlines()[0].rstrip()
                except:
                    continue
                print server.name + " - " + output


if __name__ == '__main__':
    print "Checking /etc/rsyslog.conf entries..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
