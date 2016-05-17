#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to go through decommed servers and ping check them to see if
# someone has brought them back up for some reason.
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
from server.models import AIXServer, LinuxServer
import utilities
import paramiko
from multiprocessing import Pool
django.setup()


def update_server(server):

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

    server_list = AIXServer.objects.filter(decommissioned=False)
    pool = Pool(20)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

