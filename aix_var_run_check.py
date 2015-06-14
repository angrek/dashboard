#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to get AIX total device count
#
# This is just to get a count, and not to be put in the database
# All active AIX servers, excluding VIO servers and HA duplicate devices
# do not matter per Ashfaq's request
#
# Boomer Rehfield - 12/24/2014
#
#########################################################################

import os
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import LinuxServer, AIXServer, Errpt
import utilities
django.setup()



def update_server():

    #right now we are just getting these for the non-VIO servers
    server_list = LinuxServer.objects.filter(active=True, exception=False).exclude(name__contains='vio')[:30]

    total_devices  = 0
    for server in server_list:

        print "========================================"
        print server
        if utilities.ping(server):

            client = SSHClient()
            if utilities.ssh(server, client):

                stdin, stdout, stderr = client.exec_command('ls -l /var/run | grep dzdo')
                temp = stdout.readlines()
                for line in temp:
                    print line




#start execution
if __name__ == '__main__':
    print "Getting devices..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    from server.models import AIXServer
    update_server()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
