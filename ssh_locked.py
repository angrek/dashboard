#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to unlock my account on AIX servers
#  -usually happens on new builds
#
# Boomer Rehfield - 4/26/2016
#
#########################################################################

import os

# these are need in django 1.7 and needed vs the django settings command
import django
from django.utils import timezone

from server.models import AIXServer

django.setup()


def update_server():

    # server_list = AIXServer.objects.filter(name__contains='uts0')
    server_list = AIXServer.objects.filter(decommissioned=False, active=True, exception=True)

    for server in server_list:

        command = 'dzdo ssh -q ' + server.name + ' /scripts/unlockuser.sh wrehfiel'
        os.system(command)


if __name__ == '__main__':
    print "unlocking your account..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
