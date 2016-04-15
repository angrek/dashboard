#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve SSL versions on the servers and drop them into Django dashboard
#
# Boomer Rehfield - 8/7/2014
#
#########################################################################

import os
import re
from ssh import SSHClient
import paramiko
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

            stdin, stdout, stderr = client.exec_command('lslpp -l | grep -i openssl.base')
            #this is going to pull 4 different parts of ssl, we just need the base
            rows = stdout.readlines()
            if rows:
                row = rows[0]
                #split the lines and grab the first one
                temp = row.split("\r")[0]
                p = re.compile(r' +')
                temp2 = p.split(temp)
                ssl = temp2[2]
                #if existing value is the same, don't update
                if str(ssl) != str(server.ssl):
                    utilities.log_change(server, 'SSL', str(server.ssl), str(ssl))
                    AIXServer.objects.filter(name=server).update(ssl=ssl, modified=timezone.now())


#start execution
if __name__ == '__main__':
    print "Checking SSL versions..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = AIXServer.objects.filter(decommissioned=False)
    pool = Pool(30)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
