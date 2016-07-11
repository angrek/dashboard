#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to update ping and ssh status in the database
#
# Boomer Rehfield - 8/7/2015
#
#########################################################################

import os
from paramiko import SSHClient

# these are need in django 1.7 and needed vs the django settings command
from django.utils import timezone
import django

from server.models import LinuxServer
# from server.models import AIXServer
import utilities

django.setup()


def update_server():

    server_list = LinuxServer.objects.filter(decommissioned=False, active=True, exception=True, zone=1)

    for server in server_list:

        if utilities.ping(server):

            client = SSHClient()

            if utilities.ssh(server, client):
                pass

if __name__ == '__main__':
    print "Checking Bash versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
