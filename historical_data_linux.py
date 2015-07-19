#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to copy and create historical data for the Linux servers 
#
# Boomer Rehfield - 1/28/2014
#
#########################################################################

import os, datetime
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import LinuxServer, HistoricalLinuxData
import utilities

django.setup()


def update_server():
    server_list = LinuxServer.objects.all()

    for server in server_list:
        date = datetime.date.today()
        #this was only here for testing but leaving it for some reason...?
        #date = datetime.date.today() - datetime.timedelta(days=1)
        
        #We only want one entry per day here
        HistoricalLinuxData.objects.get_or_create(date=date, name=server, vmware_cluster=server.vmware_cluster, adapter=server.adapter, active=server.active, exception=server.exception, decommissioned=server.decommissioned, created=server.created, ip_address=server.ip_address, zone=server.zone, os=server.os, os_level=server.os_level, memory=server.memory, cpu=server.cpu, centrify=server.centrify, xcelys=server.xcelys, bash=server.bash, ssl=server.ssl, java=server.java, netbackup=server.netbackup, rsyslog=server.rsyslog)



#start execution
if __name__ == '__main__':
    print "Copying Historical Linux Data..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

