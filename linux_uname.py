#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve uname (for some reason...??)
#
# Boomer Rehfield - 11/13/2015
#
# THIS IS NOT IN THE DATABASE!
#########################################################################

import os
import paramiko
from multiprocessing import Pool

# these are need in django 1.7 and needed vs the django settings command
from django.utils import timezone
import django

from server.models import LinuxServer
import utilities
os.environ['DJANGO_SETTINGS_MODULE'] = 'dashboard.settings'
django.setup()


def update_server(server):

    if utilities.ping(server):

        client = paramiko.SSHClient()
        if utilities.ssh(server, client):
            print server.name
            command = 'uname -a'
            stdin, stdout, stderr = client.exec_command(command)
            uname = stdout.readlines()[0].rstrip()

            print uname
            # check existing value, if it exists, don't update
            # if str(bash_version) != str(server.bash):
            #    utilities.log_change(server, 'bash', str(server.bash), str(bash_version))
            #    LinuxServer.objects.filter(name=server, exception=False, active=True).update(bash=bash_version, modified=timezone.now())


if __name__ == '__main__':
    print "Checking Uname..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = LinuxServer.objects.filter(decommissioned=False)

    pool = Pool(20)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
