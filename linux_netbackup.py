#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve netbackup version and drop them into Django dashboard
#
# Boomer Rehfield - 11/18//2014
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

            print server
            stdin, stdout, stderr = client.exec_command('[ -f /usr/openv/netbackup/bin/version ] && cat /usr/openv/netbackup/bin/version || echo "None"')
            print stdout

            try:
                netbackup_version = stdout.readlines()[0]
            except:
                netbackup_version = 'None'

            netbackup_version = re.sub('NetBackup-RedHat', '', netbackup_version)

            # check existing value, if it exists, don't update
            if str(netbackup_version) != str(server.netbackup):
                utilities.log_change(server, 'NetBackup', str(server.netbackup), str(netbackup_version))
                LinuxServer.objects.filter(name=server, exception=False, active=True).update(netbackup=netbackup_version, modified=timezone.now())


if __name__ == '__main__':
    print "Checking Netbackup versions..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = LinuxServer.objects.filter(decommissioned=False, active=True)
    pool = Pool(20)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
