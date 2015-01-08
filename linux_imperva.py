#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve Linux imperva versions and drop them into Django dashboard
#
# Boomer Rehfield - 11/13/2014
#
#########################################################################

import os
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import LinuxServer
import utilities
import dashboard_logging
django.setup()
import re


def update_server():
    #server_list = LinuxServer.objects.all()
    server_list = LinuxServer.objects.filter(decommissioned=False)
    #server_list = LinuxServer.objects.filter(name='d1bwadb')
    #server_list = LinuxServer.objects.filter(name__contains='db')

    for server in server_list:

        if utilities.ping(server):

            client = SSHClient()
            if utilities.ssh(server, client):
                print server.name
                command = 'lslpp -L | grep -i imper'
                stdin, stdout, stderr = client.exec_command(command)
                test = stdout.readlines()

                try:
                    output = test[0].rstrip()
                    imperva_version = ' '.join(output.split())
                    imperva_version = imperva_version.split(" ")[1].rstrip()
                    print imperva_version

                    #check existing value, if it exists, don't update
                    if str(imperva_version) != str(server.imperva):
                        dashboard_logging.log_change(str(server), 'Imperva', str(server.imperva), str(imperva_version))
                        LinuxServer.objects.filter(name=server).update(imperva=imperva_version, modified=timezone.now())
                except:
                    imperva_version = 'None'
                    print imperva_version
                    if str(imperva_version) != str(server.imperva):
                        dashboard_logging.log_change(str(server), 'Imperva', str(server.imperva), str(imperva_version))
                        LinuxServer.objects.filter(name=server).update(imperva=imperva_version, modified=timezone.now())



#start execution
if __name__ == '__main__':
    print "Checking Imperva versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

