#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve Xcelys versions and drop them into Django dashboard
#
# Boomer Rehfield - 8/7/2014
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
import test_server
import dashboard_logging
django.setup()


def update_server():

    server_list = AIXServer.objects.all()
    #server_list = AIXServer.objects.filter(name='u3midcap2')

    for server in server_list:

        if test_server.ping(server):

            client = SSHClient()
            if test_server.ssh(server, client):

                stdin, stdout, stderr = client.exec_command('[ -f /opt/xcelys/version ] && cat /opt/xcelys/version || echo "None"')
                temp_xcelys_version = stdout.readlines()[0]

                #need to cut the string down
                xcelys_version = temp_xcelys_version[36:-16]
                 
                #check existing value, if it exists, don't update
                if str(xcelys_version) != str(server.xcelys):
                    dashboard_logging.log_change(str(server), 'Xcelys', str(server.xcelys), str(xcelys_version))
                    AIXServer.objects.filter(name=server, exception=False, active=True).update(xcelys=xcelys_version, modified=timezone.now())




#start execution
if __name__ == '__main__':
    print "Checking Xcelys versions..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
