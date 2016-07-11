#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to check NFS mounts on our Linux hosts
#
# Boomer Rehfield - 06/20/2016
#
#########################################################################

import os
from paramiko import SSHClient
from multiprocessing import Pool

# these are need in django 1.7 and needed vs the django settings command
import django
from django.utils import timezone

from server.models import LinuxServer
import utilities
django.setup()


def update_server(server):

    if utilities.ping(server):

        client = SSHClient()
        if utilities.ssh(server, client):
            command = 'dzdo cat /etc/fstab | grep nfs | grep -v netdev | grep -v "#"'
            stdin, stdout, stderr = client.exec_command(command)
            lines = stdout.readlines()
            for line in lines:
                print '------------------------------------------------------'
                print server.name + ' - ' + line.rstrip()
                test = ' '.join(line.split())
                test = test.split(' ')[1]
                print test

                command = 'df | grep ' + test
                stdin, stdout, stderr = client.exec_command(command)
                output = stdout.readlines()
                yes = 0
                for li in output:
                    if li:
                        print "MOUNTED"
                        yes = 1
                if not yes:
                    print "NOT MOUNTED"


if __name__ == '__main__':
    print "Checking NFS mounts..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = LinuxServer.objects.filter(decommissioned=False, active=True, zone=2)

    pool = Pool(1)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
