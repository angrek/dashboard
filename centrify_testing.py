#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script for centrify testing
#
# Boomer Rehfield - 6/20/2015
#
#########################################################################

import os
# from ssh import SSHClient

# these are need in django 1.7 and needed vs the django settings command
import django
from django.utils import timezone

# from server.models import AIXServer, CentrifyUserCountAIX
# from server.models import CentrifyUserCountLinux
django.setup()


def update_server():

    # run_time=str(timezone.now())
    # server_list = AIXServer.objects.filter(decommissioned=False, active=True, exception=False).exclude(name__contains='vio')

    # CentrifyUserCountAIX.objects.create(run_time=run_time, name=server, user_count=user_count)

    # print server.name
    # print user_count
    # if it's the same version, we don't need to update the record
    # if str(user_count) != str(server.centrify_user_count):

    # CentrifyUserCountAIX.objects.create(run_time=run_time, name=server, user_count=user_count)

    # utilities.log_change(server, 'Centrify user count', str(server.centrify_user_count), str(user_coutn))
    pass


if __name__ == '__main__':
    print "Checking centrify version..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    update_server()
    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
