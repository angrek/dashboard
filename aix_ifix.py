#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve AIX ifix info
#
# Boomer Rehfield - 4/20/2015
#
#########################################################################

import os
from paramiko import SSHClient
from multiprocessing import Pool

# these are need in django 1.7 and needed vs the django settings command
from django.utils import timezone
import django

from server.models import AIXServer
import utilities
django.setup()


def update_server(server):

    if utilities.ping(server):

        client = SSHClient()
        if utilities.ssh(server, client):
            print server.name
            # with the vio servers we want the ios.level rather than the os_level
            command = 'dzdo emgr -l | grep lquerylv'
            stdin, stdout, stderr = client.exec_command(command)
            if stdout.readlines():
                print "yes"
                if server.ifix is False:
                    utilities.log_change(server, 'ifix', 'False', 'True')
                    AIXServer.objects.filter(name=server).update(ifix=True, modified=timezone.now())
            else:
                print "no"
                if server.ifix is True:
                    utilities.log_change(server, 'ifix', 'True', 'False')
                    AIXServer.objects.filter(name=server).update(ifix=False, modified=timezone.now())
            # need rstrip() because there are extra characters at the end

            # check existing value, if it exists, don't update
            # if str(oslevel) != str(server.os_level):
            #    utilities.log_change(server, 'oslevel', str(server.os_level), str(oslevel))
            #    AIXServer.objects.filter(name=server, exception=False, active=True).update(os_level=oslevel, modified=timezone.now())


if __name__ == '__main__':
    print "Checking ifix info..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = AIXServer.objects.filter(decommissioned=False).exclude(name__contains='vio')

    pool = Pool(20)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
