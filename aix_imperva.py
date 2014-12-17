#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve Imperva versions and drop them into Django dashboard
#
# Boomer Rehfield - 10/30/2014
#
#########################################################################

import os
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer
import test_server
import dashboard_logging
django.setup()
import re


def update_server():

    server_list = AIXServer.objects.all()
    #server_list = AIXServer.objects.filter(name='d1bwadb')
    #server_list = ['d1vio01', 'd1vio01']
    #server_list = AIXServer.objects.filter(name__contains='db')
    counter = 0

    for server in server_list:

        if test_server.ping(server):

            client = SSHClient()
            if test_server.ssh(server, client):

                command = 'lslpp -L | grep -i imper'
                stdin, stdout, stderr = client.exec_command(command)
                test = stdout.readlines()

                #I think this is split differently because of the problem with the command output. I'll have to test. FIXME
                try:
                    output = test[0].rstrip()
                    imperva_version = ' '.join(output.split())
                    imperva_version = imperva_version.split(" ")[1].rstrip()

                    #check existing value, if it exists, don't update
                    if str(imperva_version) != str(server.imperva):
                        dashboard_logging.log_change(str(server), 'Imperva', str(server.imperva), str(imperva_version))
                        AIXServer.objects.filter(name=server).update(imperva=imperva_version, modified=timezone.now())

                except:
                    imperva_version = 'Not installed'
                    if str(imperva_version) != str(server.imperva):
                        dashboard_logging.log_change(str(server), 'Imperva', str(server.imperva), str(imperva_version))
                        AIXServer.objects.filter(name=server).update(imperva=imperva_version, modified=timezone.now())



#start execution
if __name__ == '__main__':
    print "Checking Imperva versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

