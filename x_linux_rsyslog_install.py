#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to install rsyslog
#
# Boomer Rehfield - 2/25/2015
#
#########################################################################

import os
import time
from paramiko import SSHClient

# these are need in django 1.7 and needed vs the django settings command
from django.utils import timezone
import django

from server.models import LinuxServer
import utilities
django.setup()


def update_server():

    # zone = NonProduction = 1
    server_list = LinuxServer.objects.filter(zone=2, decommissioned=False, rsyslog='None')

    for server in server_list:

        if utilities.ping(server):

            client = SSHClient()
            if utilities.ssh(server, client):

                # get syslog version first
                print '------------------------------------'
                print server.name
                print "Current rsyslog version:"
                print server.rsyslog
                old_version = server.rsyslog

                # try installing it
                command = 'dzdo yum install rsyslog -y'
                stdin, stdout, stderr = client.exec_command(command)

                print 'sleeping 7 seconds for the yum db to update'
                time.sleep(15)
                # we've installed it, let's get rsyslog version now and update the database
                command = 'dzdo rpm -qa | grep rsyslog | uniq'
                stdin, stdout, stderr = client.exec_command(command)
                print "New rsyslog version:"

                try:
                    rsyslog_version = stdout.readlines()[0]
                    print str(rsyslog_version).rstrip()
                except:
                    rsyslog_version = "None"
                    print "Some sort of error here."

                # check existing value, if it exists, don't update
                if str(rsyslog_version) != old_version:
                    utilities.log_change(server, 'rsyslog', str(server.rsyslog), str(rsyslog_version))
                    LinuxServer.objects.filter(name=server).update(rsyslog=str(rsyslog_version).rstrip(), modified=timezone.now())
                    print "Database Updated++++++++++"

                # command = 'smbd -V'
                # stdin, stdout, stderr = client.exec_command(command)
                # bash_version = stdout.readlines()[0].rstrip()
                # print smbd


if __name__ == '__main__':
    print "Checking and installing rsyslog."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
