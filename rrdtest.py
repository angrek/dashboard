#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
#  RRDTool import test
#
# Boomer Rehfield - 8/10/2015
#
#########################################################################

import os, sys
from ssh import SSHClient
import paramiko
import utilities
from django.utils import timezone
from subprocess import call, check_output


from django.contrib.admin.models import LogEntry

#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import LinuxServer, Zone, Frame, Stack
from server.models import Relationships
#import logging
django.setup()

#logging.basicConfig( level=logging.INFO )

def populate():

    server_list = LinuxServer.objects.filter(name='p1metrix')

    header1 = 'curr_proc_units'
    header2 = 'entitled_cycles'
    header3 = 'capped_cycles'
    header4 = 'uncapped_cycles'

    for server in server_list:

        if utilities.ping(server):

            client = SSHClient()

            if utilities.ssh(server, client):
                stdin, stdout, stderr = client.exec_command('dzdo rrdtool dump /home/lpar2rrd/lpar2rrd/data/795B-9119-FHB-SN02764FR/phmc02/p1midcap.rrm')
                #frames = stdout.readlines()[0]
                output = stdout.readlines()
                for line in output:
                    #wait for the first 
                    print line



#start execution
if __name__ == '__main__':
    print "Starting populations..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    populate()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)




