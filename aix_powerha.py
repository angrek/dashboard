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
                if re.search("is not on file", output):
                    my_output = "None"
                elif re.search("ST_STABLE", output):
                    my_output = "STABLE"
                elif re.search("Current state", output):
                    my_output = ("Current state: ", "", output)
                else:
                    my_output = "Uncertain"

                print '--------'
                print server
                print output
                print my_output

                #check existing value, if it exists, don't update
                if my_output != str(server.powerha):
                    utilities.log_change(str(server), 'powerha', str(server.powerha), str(my_output))

                    AIXServer.objects.filter(name=server).update(powerha=my_output, modified=timezone.now())



#start execution
if __name__ == '__main__':
    print "Checking for PowerHA services..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

