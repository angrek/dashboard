#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve Target Memory Expansion Factor
#
# Boomer Rehfield - 3/12/2015
#
#########################################################################

import os
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer
from multiprocessing import Pool
import utilities

django.setup()


def update_server(server):

    if utilities.ping(server):
        
        client = SSHClient()
        if utilities.ssh(server, client):

            print "======================="
            print server.name
            command = 'lparstat -i | grep "Target Memory Expansion Factor"'
            stdin, stdout, stderr = client.exec_command(command)
            tmef = stdout.readlines()[0].rstrip()
            tmef = tmef.split()[5]
            if tmef is '-':
                tmef = 0.00
            tmef = float(tmef)
            print "======================="
            print server.name
            print tmef

            #check existing value, if it exists, don't update
            if str(tmef) != str(server.tmef):
                utilities.log_change(server, 'tmef', str(server.tmef), str(tmef))

                AIXServer.objects.filter(name=server).update(tmef=tmef, modified=timezone.now())



#start execution
if __name__ == '__main__':
    print "Checking Target Memory Expansion Factor..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = AIXServer.objects.filter(decommissioned=False)
    pool = Pool(30)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

