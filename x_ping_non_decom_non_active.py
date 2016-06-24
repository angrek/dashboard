#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to go through Lizardfish and figure out what servers can be decommed
#
# Boomer Rehfield - 9/21/2015
#
#########################################################################

import os
from subprocess import check_output

# these are need in django 1.7 and needed vs the django settings command
import django
from django.utils import timezone

from server.models import LinuxServer
import utilities

django.setup()


def update_server():

    # Original ping sweep script that just chained both AIX and Linux together
    # don't really want to chain them all together so I can work on one list at a time
    # server_list1 = AIXServer.objects.filter(decommissioned=False, active=False)
    # server_list2 = LinuxServer.objects.filter(decommissioned=False, active=False)
    # server_list = list(chain(server_list1, server_list2))

    server_list = LinuxServer.objects.filter(decommissioned=False, active=False)

    # This one is to just go through the decoms and see if any have been brought back to life
    # server_list = LinuxServer.objects.filter(decommissioned=Truye)

    for server in server_list:

        # nslookup. If this fails it will simply return a blank.

        ns_command = 'nslookup ' + str(server.name).rstrip() + ' | grep Address | grep -v "#" '
        try:
            ip_address = check_output(ns_command, shell=True)
            ip_address = str(ip_address[9:]).rstrip()
        except:
            ip_address = '0.0.0.0'

        if ip_address == '0.0.0.0':
            print str(server.name) + " - " + ip_address
        else:
            if utilities.ping(server):
                print str(server.name) + " - " + ip_address + " - ping good"
            else:
                print str(server.name) + " - " + ip_address + " - ping failed"


if __name__ == '__main__':
    print "Checking server IP addresses and ping tests..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
