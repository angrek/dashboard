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
from itertools import chain
#these are need in django 1.7 and needed vs the django settings command
import django
from django.utils import timezone
from dashboard import settings
from server.models import AIXServer, LinuxServer
import utilities
import paramiko
django.setup()


def update_server():

    server_list1 = AIXServer.objects.filter(decommissioned=True)
    server_list2 = LinuxServer.objects.filter(decommissioned=True)
    server_list = list(chain(server_list1, server_list2))


    for server in server_list:
        #counter += 1
        #print str(counter) + ' - ' + str(server)
        print server.name
        if utilities.ping(server):
            print "good"
        else:
            print "no ping"


#start execution
if __name__ == '__main__':
    print "Checking Bash versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

