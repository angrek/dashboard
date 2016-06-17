#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to check for dzdo directories in /var/run
# (Centrify upgrade issue)
#
#
# Boomer Rehfield - 2/24/2016
#
#########################################################################

import os
from ssh import SSHClient
from multiprocessing import Pool

# these are need in django 1.7 and needed vs the django settings command
from django.utils import timezone
import django

from server.models import AIXServer
import utilities
django.setup()


def update_server(server):

    if utilities.ping(server):

        client = SSHClient()
        if utilities.ssh(server, client):

            stdin, stdout, stderr = client.exec_command('ls -l /var/run | grep dzdo')
            temp = stdout.readlines()
            for line in temp:
                if line:
                    print "========================================"
                    print server
                    print line


if __name__ == '__main__':
    print "Checking /var/run..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = AIXServer.objects.filter(decommissioned=False).exclude(name__contains='vio')
    pool = Pool(20)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
