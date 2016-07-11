#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve syslog and rsyslog versions and drop them into Django
#
# Boomer Rehfield - 4/15/2015
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

            # get syslog version first
            print '------------------------------------'
            print server.name
            command = 'dzdo rpm -qa | grep sysklog | uniq'
            stdin, stdout, stderr = client.exec_command(command)

            try:
                syslog_version = stdout.readlines()[0].rstrip()
                syslog_version = re.sub(r'sysklogd-', '', syslog_version)
            except:
                syslog_version = "None"
            print syslog_version

            # get rsyslog version now
            command = 'dzdo rpm -qa | grep rsyslog | grep -v mmjson | grep -v mysql | uniq'
            stdin, stdout, stderr = client.exec_command(command)

            try:
                rsyslog_version = stdout.readlines()[0].rstrip()
                rsyslog_version = re.sub(r'.x86_64', '', rsyslog_version)
                rsyslog_version = re.sub(r'rsyslog-', '', rsyslog_version)
            except:
                rsyslog_version = "None"
            print rsyslog_version

            # check existing value, if it exists, don't update
            if str(syslog_version) != str(server.syslog):
                utilities.log_change(server, 'syslog', str(server.syslog), str(syslog_version))
                LinuxServer.objects.filter(name=server).update(syslog=syslog_version, modified=timezone.now())
            if str(rsyslog_version) != str(server.rsyslog):
                utilities.log_change(server, 'rsyslog', str(server.rsyslog), str(rsyslog_version))
                LinuxServer.objects.filter(name=server).update(rsyslog=rsyslog_version, modified=timezone.now())


if __name__ == '__main__':
    print "Checking syslog versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = LinuxServer.objects.filter(decommissioned=False)

    pool = Pool(20)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
