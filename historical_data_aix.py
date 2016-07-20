#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to copy and create historical data for the AIX servers
#
# Boomer Rehfield - 1/28/2014
#
#########################################################################

import os
import datetime
from datetime import date

# these are need in django 1.7 and needed vs the django settings command
from django.utils import timezone
import django

from server.models import AIXServer, HistoricalAIXData

django.setup()


def update_server():

    server_list = AIXServer.objects.filter(decommissioned=False)

    for server in server_list:

        my_date = datetime.date.today()
        print my_date

        # this was only here for testing but leaving it for some reason...?
        # date = datetime.date.today() - datetime.timedelta(days=1)
        # We only want one entry per day here

        HistoricalAIXData.objects.get_or_create(date=my_date, name=server, frame=server.frame, active=server.active, exception=server.exception, decommissioned=server.decommissioned, created=server.created, ip_address=server.ip_address, zone=server.zone, os_level=server.os_level, centrify=server.centrify, aix_ssh=server.aix_ssh, cent_ssh=server.cent_ssh, xcelys=server.xcelys, bash=server.bash, ssl=server.ssl, imperva=server.imperva, netbackup=server.netbackup, rsyslog=server.rsyslog, emc_clar=server.emc_clar, emc_sym=server.emc_sym)


if __name__ == '__main__':
    print "Copying Historical AIX Data..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
