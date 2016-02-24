#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve Linux SSL versions on the servers and drop them into Django dashboard
#
# Boomer Rehfield - 11/13/2014
#
#########################################################################

import os
import re
from ssh import SSHClient
import paramiko
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
import utilities
import utilities
django.setup()


def update_server():

    server_list = LinuxServer.objects.filter(decommissioned=False)

    for server in server_list:
            
        if utilities.ping(server):

            client = SSHClient()
            if utilities.ssh(server, client):

                stdin, stdout, stderr = client.exec_command('dzdo rpm -qa | grep openssl | grep -v devel | uniq | tail -n 1')
                #this is going to pull 4 different parts of ssl, we just need the base
                rows = stdout.readlines()
                ssl = str(rows[0]).rstrip().rstrip()
                print ssl
                #

                #cut off the beginning and end, not really needed and saves space on the spreadsheet view.
                ssl = re.sub('openssl-', '', ssl)
                ssl = re.sub('.x86_64', '', ssl)

                #if existing value is the same, don't update
                if str(ssl) != str(server.ssl):
                    utilities.log_change(server, 'SSL', str(server.ssl), str(ssl))
                    LinuxServer.objects.filter(name=server, exception=False, active=True).update(ssl=ssl, modified=timezone.now())



#start execution
if __name__ == '__main__':
    print "Checking SSL versions..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    from server.models import LinuxServer
    update_server()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
