#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to get total cpu and mem data for VMs
#
# Boomer Rehfield - 7/15/2016
#
#########################################################################

import os

# these are need in django 1.7 and needed vs the django settings command
import django
from django.utils import timezone

from server.models import LinuxServer
import utilities
django.setup()


def update_server():

    server_list = LinuxServer.objects.filter(decommissioned=False).exclude(vmware_cluster='Physical')

    total_cpus = 0
    total_mem = 0

    for server in server_list:

        print server.name
        print server.cpu
        print server.memory

        total_cpus = total_cpus + int(server.cpu)
        total_mem = total_mem + int(server.memory)

    print "====================================="
    print "Total CPUS: " + str(total_cpus)
    print "Total Mem:  " + str(total_mem)

if __name__ == '__main__':
    print "Checking Bash versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
