#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve AIX OS levels
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
import utilities
from multiprocessing import Pool
django.setup()


def update_server(server):

    if utilities.ping(server):

        client = SSHClient()
        if utilities.ssh(server, client):
            print server.name
            #with the vio servers we want the ios.level rather than the os_level
            vio_servers = AIXServer.objects.filter(name__contains='vio')
            hmc_servers = AIXServer.objects.filter(name__contains='hmc')
            if server in vio_servers:
                command = 'cat /usr/ios/cli/ios.level'
            elif server in hmc_servers:
                command = 'lshmc -V | grep Release'
            else:
                command = 'dzdo oslevel -s'
            stdin, stdout, stderr = client.exec_command(command)

            #need rstrip() because there are extra characters at the end
            oslevel = stdout.readlines()[0].rstrip()

            if server in hmc_servers:
                oslevel = "HMC " + oslevel
            
            if server in vio_servers:
                oslevel = "VIO " + oslevel

            #check existing value, if it exists, don't update
            if str(oslevel) != str(server.os_level):
                utilities.log_change(server, 'oslevel', str(server.os_level), str(oslevel))
                AIXServer.objects.filter(name=server, exception=False, active=True).update(os_level=oslevel, modified=timezone.now())



#start execution
if __name__ == '__main__':
    print "Checking OS versions..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = AIXServer.objects.filter(decommissioned=False)
    pool = Pool(20)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
