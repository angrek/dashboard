#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve the Centrify versions of SSH on the servers
#
# Boomer Rehfield - 12/3/2014
#
#########################################################################

import os
import re
from ssh import SSHClient
from multiprocessing import Pool

# these are need in django 1.7 and needed vs the django settings command
from django.utils import timezone
import django

from server.models import AIXServer
import utilities
django.setup()


def update_server(server):

    if utilities.ping(server):

        client = SSHClient()
        if utilities.ssh(server, client):

            stdin, stdout, stderr = client.exec_command('lslpp -l | grep -i CentrifyDC.openssh | uniq')
            # this is going to pull 4 different parts of ssl, we just need the base
            rows = stdout.readlines()

            if rows:
                row = rows[0]
                # split the lines and grab the first one
                temp = row.split("\r")[0]
                p = re.compile(r' +')
                temp2 = p.split(temp)
                ssh = temp2[2]

                # if existing value is the same, don't update
                if str(ssh) != str(server.cent_ssh):
                    utilities.log_change(server, 'Centrify SSH', str(server.cent_ssh), str(ssh))
                    AIXServer.objects.filter(name=server, exception=False, active=True).update(cent_ssh=ssh, modified=timezone.now())


if __name__ == '__main__':
    print "Checking Centrify SSH versions..."
    start_time = timezone.now()

    server_list = AIXServer.objects.filter(decommissioned=False)
    pool = Pool(20)
    pool.map(update_server, server_list)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
