#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve Linux glibc versions on
# the servers and drop them into Django dashboard
#
# Boomer Rehfield - 2/24/2016
#
#########################################################################

import os
import re
from paramiko import SSHClient
from multiprocessing import Pool

# these are need in django 1.7 and needed vs the django settings command
from django.utils import timezone
import django

from server.models import LinuxServer
import utilities

django.setup()


def update_server(server):

    if utilities.ping(server):

        client = SSHClient()

        if utilities.ssh(server, client):

            stdin, stdout, stderr = client.exec_command('dzdo rpm -qa | grep glibc | grep -v devel | grep -v common | grep -v compat | grep -v static | grep -v headers | uniq | tail -n 1')
            # this is going to pull 4 different parts of ssl, we just need the base
            glibc = stdout.readlines()[0]
            # glibc = str(rows[0]).rstrip().rstrip()

            # cut off the beginning and end, not really needed and saves space on the spreadsheet view.
            glibc = re.sub('glibc-', '', glibc)
            glibc = re.sub('.x86_64', '', glibc)
            glibc = re.sub('.i686', '', glibc)

            print glibc

            # if existing value is the same, don't update

            if str(glibc) != str(server.glibc):
                utilities.log_change(server, 'glibc', str(server.glibc), str(glibc))
                LinuxServer.objects.filter(name=server, exception=False, active=True).update(glibc=glibc, modified=timezone.now())


if __name__ == '__main__':
    print "Checking glibc versions..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = LinuxServer.objects.filter(decommissioned=False)
    pool = Pool(20)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
