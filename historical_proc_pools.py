#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to copy and create historical data for the AIX Proc Pools
#
# Boomer Rehfield - 6/24/2015
#
#########################################################################

import os
import datetime

# these are need in django 1.7 and needed vs the django settings command
import django
from django.utils import timezone

from server.models import AIXProcPool, HistoricalAIXProcPoolData

django.setup()


def update_server():

    pool_list = AIXProcPool.objects.all()

    for pool in pool_list:

        my_date = datetime.date.today()

        try:
            HistoricalAIXProcPoolData.objects.get_or_create(date=my_date, frame=pool.frame, pool_name=pool.pool_name, max_proc_units=pool.max_proc_units, used_proc_units=pool.used_proc_units, curr_procs=pool.curr_procs)
        except:
            pass


if __name__ == '__main__':
    print "Copying Historical AIX Proc Pool Data...Please have a seat over here..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
