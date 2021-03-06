#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve Frame firmware levels
#
# Boomer Rehfield - 3/16/2015
#
#########################################################################

import os
import re
from paramiko import SSHClient

# these are need in django 1.7 and needed vs the django settings command
from django.utils import timezone
import django

from server.models import AIXServer, Frame
import utilities

django.setup()


def update_server():

    frame_list = Frame.objects.all().exclude(name='None')

    for frame in frame_list:

        server_list = AIXServer.objects.filter(active=True, exception=False, decommissioned=False, frame=frame).exclude(name__contains='vio')
        print "======================="
        print frame.name

        for server in server_list[:1]:

            print server.name

            if utilities.ping(server):

                client = SSHClient()
                if utilities.ssh(server, client):

                    command = 'dzdo lsmcode -c | grep temporary | grep -v booted'
                    stdin, stdout, stderr = client.exec_command(command)
                    firmware_version = stdout.readlines()[0].rstrip()
                    if re.search("FW", firmware_version):
                        firmware_version = firmware_version.split(' ')[8]
                    else:
                        firmware_version = firmware_version.split(' ')[7]

                    print firmware_version
                    firmware_version = firmware_version[1:-1]
                    print firmware_version

                    # check existing value, if it exists, don't update
                    if firmware_version != frame.firmware_version:
                        # utilities.log_change(frame, 'firmware version', str(frame.firmware_version), str(firmware_version))

                        Frame.objects.filter(name=frame.name).update(firmware_version=firmware_version)


if __name__ == '__main__':
    print "Checking Frame firmware versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
