#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve netbackup version and drop them into Django dashboard
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
from server.models import LinuxServer
import re
import utilities
django.setup()


def update_server():
    #server_list = LinuxServer.objects.all()
    server_list = LinuxServer.objects.filter(decommissioned=False)
    #server_list = LinuxServer.objects.filter(name='u3midcap2')

    for server in server_list:

        if utilities.ping(server):

            client = SSHClient()
            if utilities.ssh(server, client):

                stdin, stdout, stderr = client.exec_command('[ -f /usr/openv/netbackup/bin/version ] && cat /usr/openv/netbackup/bin/version || echo "None"')
                netbackup_version = stdout.readlines()[0]

                 
                #check existing value, if it exists, don't update
                if str(netbackup_version) != str(server.netbackup):
                    utilities.log_change(str(server), 'NetBackup', str(server.netbackup), str(netbackup_version))
                    LinuxServer.objects.filter(name=server, exception=False, active=True).update(netbackup=netbackup_version, modified=timezone.now())




#start execution
if __name__ == '__main__':
    print "Checking Netbackup versions..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
