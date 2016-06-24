#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve bash versions
#
# Boomer Rehfield - 10/6/2014
#
#########################################################################

import os
from ssh import SSHClient
from multiprocessing import Pool

# this is need in django 1.7 and needed vs the django settings command
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
            command = 'rpm -qa | grep bash |grep -v doc'
            stdin, stdout, stderr = client.exec_command(command)
            try:
                bash_version = stdout.readlines()[0].rstrip()
                # check existing value, if it exists, don't update
                if str(bash_version) != str(server.bash):
                    utilities.log_change(server, 'bash', str(server.bash), str(bash_version))
                    AIXServer.objects.filter(name=server).update(bash=bash_version, modified=timezone.now())

            except:
                print "Problem getting bash version"

            client.close()

if __name__ == '__main__':
    print "Checking Bash versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    # server_list = AIXServer.objects.filter(decommissioned=False)
    server_list = AIXServer.objects.filter(decommissioned=False, name__contains='vio')
    pool = Pool(20)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
