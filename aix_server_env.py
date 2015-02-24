#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to check for env/server.env
#
# Boomer Rehfield - 2/24/2015
#
#########################################################################

import os, sys, re
from subprocess import *
from time import strptime
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer
import utilities
from  datetime import datetime, date, timedelta
import datetime
django.setup()


def check_server():
    server_list = AIXServer.objects.filter(decommissioned=False)
    success = 0
    print server_list 
    for server in server_list:
        if utilities.ping(server):
            client = SSHClient()
            if utilities.ssh(server, client):
                stdin, stdout, stderr = client.exec_command(' [ -f /etc/env/server.env ] && echo 1 || echo 0')
                test = stdout.readlines()
                print "------------------------------------------------------------"
                if int(test[0]) == 0:
                    print "server " + server.name + " env files does NOT exist*********************"
                    AIXServer.objects.filter(name=server).update(server_env=0)
                elif int(test[0]) == 1:
                    print "server " + server.name + " is good."
                    AIXServer.objects.filter(name=server).update(server_env=1)
                    stdin, stdout, stderr = client.exec_command('cat /etc/env/server.env')
                    test = stdout.readlines()
                    output = ''
                    for line in test:
                        output = output + line
                    print output
                    AIXServer.objects.filter(name=server).update(server_env_text=output)
                else:
                    print "server " + server.name + " has no idea what it's doing."
    #if not success:
    #    subject = 'None of the servers have a /mksysbWPAR directory'
    #    print subject
    #    utilities.send_email(subject, server_list)
    #    sys.exit()
    #else:
    #    return server


#start execution
if __name__ == '__main__':
    print "Checking for server.env files..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    check_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

