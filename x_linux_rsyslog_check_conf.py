#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve syslog and rsyslog versions and drop them into Django
#
# Boomer Rehfield - 2/25/2014
#
#########################################################################

import os
from paramiko import SSHClient

# these are need in django 1.7 and needed vs the django settings command
from django.utils import timezone
import django

from server.models import LinuxServer
import utilities
django.setup()


def update_server():

    server_list = LinuxServer.objects.filter(active=True, exception=False, zone=1, decommissioned=False)

    for server in server_list[:25]:

        if server.rsyslog is not 'None':

            if utilities.ping(server):

                client = SSHClient()
                if utilities.ssh(server, client):
                    print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
                    print server.name
                    print "Current syslog conf:"
                    print server.syslog

                    command = 'cat /etc/syslog.conf'
                    stdin, stdout, stderr = client.exec_command(command)
                    t = stdout.readlines()
                    for line in t:
                        print line.rstrip()

                    print '---------------------------'

                    # command = 'cat /etc/rsyslog.conf'
                    # stdin, stdout, stderr = client.exec_command(command)

                    # try changing chkconfig
                    # command = 'chkconfig --list | grep rsyslog'
                    # stdin, stdout, stderr = client.exec_command(command)
                    # t = stdout.readlines()[0]
                    # print t


if __name__ == '__main__':
    print "Checking and installing rsyslog."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
