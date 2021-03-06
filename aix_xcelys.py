#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve Xcelys versions and drop them into Django dashboard
#
# Boomer Rehfield - 8/4/2014
#
#########################################################################

import os
from paramiko import SSHClient

# these are need in django 1.7 and needed vs the django settings command
import django
from django.utils import timezone

from server.models import AIXServer
import utilities
django.setup()


def update_server():

    server_list = AIXServer.objects.filter(decommissioned=False)

    for server in server_list:

        if utilities.ping(server):

            client = SSHClient()

            if utilities.ssh(server, client):

                stdin, stdout, stderr = client.exec_command('[ -f /opt/xcelys/version ] && cat /opt/xcelys/version || echo "None"')
                temp_xcelys_version = stdout.readlines()[0]

                # need to cut the string down
                xcelys_version = temp_xcelys_version[36:-16]
                if xcelys_version is '':
                    xcelys_version = 'None'
                # check existing value, if it exists, don't update
                if str(xcelys_version) != str(server.xcelys):
                    utilities.log_change(server, 'Xcelys', str(server.xcelys), str(xcelys_version))
                    AIXServer.objects.filter(name=server, exception=False, active=True).update(xcelys=xcelys_version, modified=timezone.now())


if __name__ == '__main__':
    print "Checking Xcelys versions..."
    start_time = timezone.now()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()

    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
