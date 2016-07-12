#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script check if rsyslog is running
#
# Boomer Rehfield - 3/4/2014
#
#########################################################################

import os
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
            command = 'dzdo /sbin/service rsyslog status'
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.readlines()
            for line in output[:1]:
                if line.rstrip() == 'rsyslogd is stopped':

                    LinuxServer.objects.filter(name=server.name).update(rsyslog_r=0, modified=timezone.now())
                    print 'rsyslog is stopped'
                else:
                    LinuxServer.objects.filter(name=server.name).update(rsyslog_r=1, modified=timezone.now())
                    print 'rsyslog is running'


if __name__ == '__main__':

    print "Checking Bash versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = LinuxServer.objects.filter(decommissioned=False)

    pool = Pool(10)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
