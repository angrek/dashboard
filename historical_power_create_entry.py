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
from server.models import AIXServer
from server.models import Power7Inventory
from server.models import  HistoricalAIXData
from server.models import  HistoricalPowerInventory
import utilities

django.setup()


def update_server():
    tmp = HistoricalPowerInventory.objects.all().order_by('date')[:1]
    oldest_date = tmp[0].date
    print oldest_date
 
    date = oldest_date - datetime.timedelta(days=2)
    print date

    #data_list = HistoricalAIXData.objects.filter(date=oldest_date)
    server_list = Power7Inventory.objects.all()
    for server in server_list:
        #We only want one entry per day here
        HistoricalPowerInventory.objects.get_or_create(date=date, name=server.name, lpar_id=server.lpar_id, frame=server.frame, curr_shared_proc_pool_id=server.curr_shared_proc_pool_id, curr_proc_units=server.curr_proc_units, curr_procs=server.curr_procs, curr_mem=server.curr_mem)



#start execution
if __name__ == '__main__':
    print "Copying Historical AIX Data..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

