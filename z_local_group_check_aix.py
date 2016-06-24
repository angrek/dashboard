#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to search for local groups with 500 id
#
# Boomer Rehfield - 2/8/2016
#
#########################################################################

import os
import paramiko

# these are need in django 1.7 and needed vs the django settings command
import django
from django.utils import timezone

from server.models import AIXServer
import utilities
django.setup()


def update_server():

    server_list = AIXServer.objects.filter(decommissioned=False)

    print '-------------------'
    for server in server_list:

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
                # print bash_version.rstrip()
                # print line.rstrip()
                # print timezone.now()
                # check existing value, if it exists, don't update
                # if str(bash_version) != str(server.bash):
                #   utilities.log_change(server, 'bash', str(server.bash), str(bash_version))
                #   LinuxServer.objects.filter(name=server, exception=False, active=True).update(bash=bash_version, modified=timezone.now())


if __name__ == '__main__':
    print "Checking for groups with the 500 id...."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
