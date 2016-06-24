#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to count the number of efix's on an AIX box
#
# Boomer Rehfield - 3/4/2016
#
#########################################################################

import os
from ssh import SSHClient
from multiprocessing import Pool

# these are need in django 1.7 and needed vs the django settings command
from django.utils import timezone
import django

from server.models import AIXServer
import utilities

django.setup()


def update_server(server):

    counter = 0
    if utilities.ping(server):

        client = SSHClient()
        if utilities.ssh(server, client):

            command = 'dzdo emgr -l'
            stdin, stdout, stderr = client.exec_command(command)
            lines = stdout.readlines()
            print ""
            print "-----------------------------------"
            print server.name
            # del lines[0]
            # del lines[1]
            # del lines[2]

            for line in lines[3:-17]:
                counter = counter + 1
                print line.rstrip()

            print "Number of efixes -> " + str(counter)
            # check existing value, if it exists, don't update
            if counter != server.efix:
                utilities.log_change(server, 'efix', str(server.efix), str(counter))

                AIXServer.objects.filter(name=server).update(efix=counter, modified=timezone.now())


if __name__ == '__main__':
    print "Getting number of efixs..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = AIXServer.objects.filter(decommissioned=False)
    pool = Pool(20)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
