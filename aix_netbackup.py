#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve netbackup versions
#
# Boomer Rehfield - 11/18//2014
#
#########################################################################

import os
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer
import re
import utilities
django.setup()


def update_server():

    server_list = AIXServer.objects.filter(decommissioned=False)

    for server in server_list:

        if utilities.ping(server):

            client = SSHClient()
            if utilities.ssh(server, client):

                stdin, stdout, stderr = client.exec_command('[ -f /usr/openv/netbackup/bin/version ] && cat /usr/openv/netbackup/bin/version || echo "None"')
                netbackup_version = stdout.readlines()[0].rstrip()

                #check existing value, if it exists, don't update
                if str(netbackup_version) != str(server.netbackup):
                    utilities.log_change(str(server), 'NetBackup', str(server.netbackup), str(netbackup_version))
                    AIXServer.objects.filter(name=server).update(netbackup=netbackup_version, modified=timezone.now())



#start execution
if __name__ == '__main__':
    print "Checking Netbackup versions..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
