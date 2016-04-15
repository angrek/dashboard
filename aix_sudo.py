#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# I think I created this to find versions of sudo that were NOT 1.7.2??
#
# Boomer Rehfield - 12/28/2015
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
import paramiko
from multiprocessing import Pool
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
            
            #bash_version = re.sub(r'x86_64', '', bash_version)
            #print sudo_version
            if '1.7.2' not in sudo_version:
                inventory_list.append(server.name)
                print server.name + ' - ' + sudo_version
                #print sudo_version
            #print timezone.now()
            #check existing value, if it exists, don't update
            #if str(bash_version) != str(server.bash):
            #    utilities.log_change(server, 'bash', str(server.bash), str(bash_version))
            #    LinuxServer.objects.filter(name=server, exception=False, active=True).update(bash=bash_version, modified=timezone.now())

    print ''
    print 'Inventory file listing'
    for server in inventory_list:
        print server

#start execution
if __name__ == '__main__':
    print "Checking Bash versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = AIXServer.objects.filter(decommissioned=False)
    pool = Pool(30)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

