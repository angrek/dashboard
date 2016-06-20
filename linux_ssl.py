#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve Linux SSL versions on the servers and drop them into Django dashboard
#
# Boomer Rehfield - 11/13/2014
#
#########################################################################

import os
import re
from ssh import SSHClient
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

            # this is going to pull 4 different parts of ssl, we just need the base
            stdin, stdout, stderr = client.exec_command('dzdo rpm -qa | grep openssl | grep -v devel | uniq | tail -n 1')

            rows = stdout.readlines()
            ssl = str(rows[0]).rstrip().rstrip()

            print server.name
            print ssl

            ssl = re.sub('openssl-', '', ssl)
            ssl = re.sub('.x86_64', '', ssl)

            # if existing value is the same, don't update
            if str(ssl) != str(server.ssl):
                utilities.log_change(server, 'SSL', str(server.ssl), str(ssl))
                LinuxServer.objects.filter(name=server).update(ssl=ssl, modified=timezone.now())


if __name__ == '__main__':
    print "Checking SSL versions..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = LinuxServer.objects.filter(decommissioned=False)

    pool = Pool(20)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
