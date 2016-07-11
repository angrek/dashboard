#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to check for env/server.env
#
# Boomer Rehfield - 2/24/2015
#
#########################################################################

import os
# from subprocess import *
from paramiko import SSHClient
from subprocessing import Pool

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
            stdin, stdout, stderr = client.exec_command(' [ -f /etc/env/server.env ] && echo 1 || echo 0')
            test = stdout.readlines()
            print "------------------------------------------------------------"
            if int(test[0]) == 0:
                print "server " + server.name + " env files does NOT exist*********************"
                LinuxServer.objects.filter(name=server).update(server_env=0)
            elif int(test[0]) == 1:
                print "server " + server.name + " is good."
                LinuxServer.objects.filter(name=server).update(server_env=1)
                stdin, stdout, stderr = client.exec_command('cat /etc/env/server.env')
                test = stdout.readlines()
                output = ''
                for line in test:
                    output = output + line
                print output
                LinuxServer.objects.filter(name=server).update(server_env_text=output)
            else:
                print "server " + server.name + " has no idea what it's doing."


if __name__ == '__main__':
    print "Checking for server.env files..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = LinuxServer.objects.filter(decommissioned=False)
    pool = Pool(20)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
