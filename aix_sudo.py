#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# I think I created this to find versions of sudo that were NOT 1.7.2??
#
# Boomer Rehfield - 1/15/2016
#
#########################################################################

import os
import paramiko
from multiprocessing import Pool

# these are need in django 1.7 and needed vs the django settings command
from django.utils import timezone
import django

from server.models import AIXServer
import utilities
django.setup()


def update_server(server):

    inventory_list = []

    if utilities.ping(server):

        client = paramiko.SSHClient()
        if utilities.ssh(server, client):
            command = 'dzdo sudo -V | grep version | grep -v Sudoers'
            stdin, stdout, stderr = client.exec_command(command)
            try:
                sudo_version = stdout.readlines()[0].rstrip()
            except:
                print server.name + ' - PROBLEM!!!!!!!!'

            if '1.7.2' not in sudo_version:
                inventory_list.append(server.name)
                print server.name + ' - ' + sudo_version

    print ''
    print 'Inventory file listing'
    for server in inventory_list:
        print server

if __name__ == '__main__':
    print "Checking Bash versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = AIXServer.objects.filter(decommissioned=False)
    pool = Pool(20)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
