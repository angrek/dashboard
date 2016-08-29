#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to see if SCOM is installed and running
#
# Boomer Rehfield - 8/2/2016
#
#########################################################################

import os
import re
import paramiko

# these are need in django 1.7 and needed vs the django settings command
import django
from django.utils import timezone

from server.models import LinuxServer, AIXServer
import utilities
django.setup()


def update_server():

    aix_server_list = AIXServer.objects.filter(decommissioned=False, active=True, zone=2)
    # linux_server_list = LinuxServer.objects.filter(decommissioned=False, active=True, zone=2)

    aix_server_count = 0
    linux_server_count = 0

    aix_scom_installed = 0
    linux_scom_installed = 0

    aix_scom_running = 0
    linux_scom_running = 0

    list_aix_not_installed = []
    list_linux_not_installed = []

    list_aix_not_running = []
    list_linux_not_running = []

    for server in aix_server_list:

        if utilities.ping(server):

            client = paramiko.SSHClient()
            if utilities.ssh(server, client):

                print server.name

                aix_server_count = aix_server_count + 1

                command = "dzdo lssrc -s scx-cimd"
                stdin, stdout, stderr = client.exec_command(command)

                for line in stdout.readlines():
                    print line.rstrip()
                    if re.search('active', line):
                        aix_scom_installed += 1 
                        aix_scom_running += 1
                    if re.search('not on file', line):
                        aix_scom_installed += 1
                        list_aix_not_running.append(server.name)

                    

        print '-----------------------------'

    aix_scom_not_running = aix_server_count - aix_scom_running
    print ""
    print ""
    print "======================================"
    print "======================================"
    print "Number of AIX Servers:     " + str(aix_server_count)
    print "Number of AIX SCOM Installs: " + str(aix_scom_installed)
    print "Number of AIX SCOM Running: " + str(aix_scom_running)
    print "Number of AIX SCOM NOT Running: " + str(aix_scom_not_running)
    print "======================================"
    print "List of AIX servers where SCOM is not installed"
    print "======================================"

    for name in list_aix_not_installed:
        print name

    print "======================================"
    print "List of AIX servers where SCOM is not running"
    print "======================================"

    for name in list_aix_not_running:
        print name


if __name__ == '__main__':
    print "Production SCOM Report"
    print "----------------------"
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
