#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve samba versions and drop them into Django dashboard
#
# Boomer Rehfield - 2/25/2014
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

            print '------------------------------------'
            print server.name
            command = 'dzdo /usr/sbin/smbd -V'
            stdin, stdout, stderr = client.exec_command(command)
            try:
                samba = stdout.readlines()[0]
                print samba
            except:
                samba = "None"
                print samba

            samba = re.sub(r'Version ', '', samba)

            # check existing value, if it exists, don't update
            if str(samba) != str(server.samba):
                utilities.log_change(server, 'samba', str(server.samba), str(samba))
                LinuxServer.objects.filter(name=server).update(samba=samba, modified=timezone.now())


if __name__ == '__main__':
    print "Checking Bash versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = LinuxServer.objects.filter(decommissioned=False)

    pool = Pool(20)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
