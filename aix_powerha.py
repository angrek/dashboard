#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to check if powerHA is installed
#
# Boomer Rehfield - 2/3/2015
#
#########################################################################

import os, re
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer
import utilities

django.setup()


def update_server():

    server_list = AIXServer.objects.filter(decommissioned=False)

    counter = 0
    for server in server_list:

        if utilities.ping(server):
            
            client = SSHClient()
            if utilities.ssh(server, client):

                command = 'lssrc -ls clstrmgrES|head -1'
                stdin, stdout, stderr = client.exec_command(command)
                output = stdout.readlines()[0].rstrip()
                print 'OUTPUT =>' + output
                if re.search("is not on file", output):
                    my_output = "None"

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
                
                #elif re.search("ST_STABLE", output):
                #    my_output = "STABLE"
                #elif re.search("Current state", output):
                #    my_output = ("Current state: ", "", output)
                #else:
                #    my_output = "Uncertain"

                print '--------'
                print server
                print output
                print cluster_state
                print cluster_description

                #check existing value, if it exists, don't update
                if cluster_state != str(server.powerha):
                    utilities.log_change(server, 'powerha', str(server.powerha), str(cluster_state))

                    AIXServer.objects.filter(name=server).update(powerha=cluster_state, cluster_description=cluster_description, modified=timezone.now())
                if cluster_description != str(server.cluster_description):
                    AIXServer.objects.filter(name=server).update(cluster_description=cluster_description)
                    


#start execution
if __name__ == '__main__':
    print "Checking for PowerHA services..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

