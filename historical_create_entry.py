#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Quick script to take the oldest date, get all the server data, and
# make a complete copy of it with the previous days date. (this is for
# populating the database day by day from old LogEntry to see how
# much history we can keep before the Historical model was put in.
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
from server.models import AIXServer, HistoricalAIXData
import utilities

django.setup()


def update_server():
    tmp = HistoricalAIXData.objects.all().order_by('date')[:1]
    oldest_date = tmp[0].date
    print oldest_date
 
    date = oldest_date - datetime.timedelta(days=1)
    print date

    data_list = HistoricalAIXData.objects.filter(date=oldest_date)
    for server in data_list:
        #We only want one entry per day here
        HistoricalAIXData.objects.get_or_create(date=date, name=server.name, frame=server.frame, active=server.active, exception=server.exception, decommissioned=server.decommissioned, created=server.created, ip_address=server.ip_address, zone=server.zone, os_level=server.os_level, centrify=server.centrify, aix_ssh=server.aix_ssh, cent_ssh=server.cent_ssh, xcelys=server.xcelys, bash=server.bash, ssl=server.ssl, java=server.java, imperva=server.imperva, netbackup=server.netbackup, emc_clar=server.emc_clar, emc_sym=server.emc_sym)



#start execution
if __name__ == '__main__':
    print "Copying Historical AIX Data..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

