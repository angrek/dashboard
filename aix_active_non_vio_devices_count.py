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
from server.models import AIXServer, Errpt
import utilities
django.setup()



def update_server():
    #right now we are just getting these for the VIO servers
    server_list = AIXServer.objects.filter(active=True, exception=False).exclude(name__contains='vio')
    #server_list = AIXServer.objects.filter(name__contains='vio')
    total_devices  = 0
    for server in server_list:

        if utilities.ping(server):

            client = SSHClient()
            if utilities.ssh(server, client):
                stdin, stdout, stderr = client.exec_command('lspv | wc -l')
                temp = stdout.readlines()[0].rstrip()
                devices = int(temp)
                print server
                print devices
                total_devices += devices            
                print "Total - " + str(total_devices)




#start execution
if __name__ == '__main__':
    print "Getting devices..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    from server.models import AIXServer
    update_server()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
