#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to check if powerHA is installed
#
# Boomer Rehfield - 2/3/2015
#
#########################################################################

import os
import re
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

            command = 'lssrc -ls clstrmgrES|head -1'
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.readlines()[0].rstrip()
            print server.name
            print 'OUTPUT =>' + output

            if re.search("is not on file", output):
                cluster_state = "None"
                cluster_description = "None"
            else:
                cluster_state = re.sub('Current state: ', '', output)

                state_dict = {'ST_INIT': 'cluster configured and down',
                              'ST_JOINING': 'node joining the cluster',
                              'ST_VOTING': 'Inter-node decision state for an event',
                              'ST_RP_RUNNING': 'cluster running recovery program',
                              'ST_BARRIER': 'clstrmgr is exiting recovery program',
                              'ST_CBARRIER': 'clstrmgr is exiting recovery program',
                              'ST_UNSTABLE': 'cluster unstable',
                              'NOT_CONFIGURED': 'HA installed but not configured',
                              'RP_FAILED': 'event script failed',
                              'ST_RP_FAILED': 'event script failed',
                              'ST_STABLE': 'cluster services are running',
                              'STABLE': 'cluster services are running'}

                cluster_description = state_dict[cluster_state]

            print '--------'
            print server
            print output
            print cluster_state
            print cluster_description

            if cluster_state != str(server.powerha):
                utilities.log_change(server, 'powerha', str(server.powerha), str(cluster_state))

                AIXServer.objects.filter(name=server).update(powerha=cluster_state, cluster_description=cluster_description, modified=timezone.now())
            if cluster_description != str(server.cluster_description):
                AIXServer.objects.filter(name=server).update(cluster_description=cluster_description)


if __name__ == '__main__':
    print "Checking for PowerHA services..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = AIXServer.objects.filter(decommissioned=False)
    pool = Pool(1)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
