#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Quick ping script that will update the database. Quick on off for one host
#
# Boomer Rehfield - 6/16/2015
#
#########################################################################

import os

# these are need in django 1.7 and needed vs the django settings command
from django.utils import timezone
import django

from server.models import AIXServer
import utilities

django.setup()


def update_server():

    server_list = AIXServer.objects.filter(name__contains="u0")

    for server in server_list:

        print server.name
        if utilities.ping(server):
            print "good"
        else:
            print "no ping"


if __name__ == '__main__':
    print "Starting ping sweep..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
