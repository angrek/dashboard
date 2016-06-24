#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to search for requiretty in sudoers
#
# Boomer Rehfield - 10/23/2016
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

    print '-------------------'
    for server in server_list:

        if utilities.ping(server):

            client = paramiko.SSHClient()
            if utilities.ssh(server, client):
                command = "dzdo grep requiretty /etc/sudoers | grep -v nxmon"
                stdin, stdout, stderr = client.exec_command(command)
                try:
                    bash_version = stdout.readlines()[0].rstrip()
                except:
                    continue

                print server.name + " ->      " + bash_version.rstrip()
                # print bash_version.rstrip()
                # print line.rstrip()
                # print timezone.now()
                # check existing value, if it exists, don't update
                # if str(bash_version) != str(server.bash):
                #   utilities.log_change(server, 'bash', str(server.bash), str(bash_version))
                #   LinuxServer.objects.filter(name=server, exception=False, active=True).update(bash=bash_version, modified=timezone.now())


if __name__ == '__main__':
    print "Checking for tty in sudoers..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
