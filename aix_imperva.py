#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve Imperva versions
#
# Boomer Rehfield - 11/2/2014
#
#########################################################################

import os
from ssh import SSHClient
from multiprocessing import Pool

# these are need in django 1.7 and needed vs the django settings command
import django
from django.utils import timezone

from server.models import AIXServer
import utilities

django.setup()


def update_server(server):

    if utilities.ping(server):

        client = SSHClient()
        if utilities.ssh(server, client):
            print server.name
            command = 'lslpp -L | grep -i imper'
            stdin, stdout, stderr = client.exec_command(command)
            test = stdout.readlines()

            try:
                output = test[0].rstrip()
                imperva_version = ' '.join(output.split())
                imperva_version = imperva_version.split(" ")[1].rstrip()
                print imperva_version

                # check existing value, if it exists, don't update
                if str(imperva_version) != str(server.imperva):
                    utilities.log_change(server, 'Imperva', str(server.imperva), str(imperva_version))
                    AIXServer.objects.filter(name=server).update(imperva=imperva_version, modified=timezone.now())

            except:
                imperva_version = 'None'
                print imperva_version
                if str(imperva_version) != str(server.imperva):
                    utilities.log_change(server, 'Imperva', str(server.imperva), str(imperva_version))
                    AIXServer.objects.filter(name=server).update(imperva=imperva_version, modified=timezone.now())


if __name__ == '__main__':
    print "Checking Imperva versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = AIXServer.objects.filter(decommissioned=False)

    pool = Pool(20)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
