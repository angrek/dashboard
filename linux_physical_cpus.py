#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve Python versions 
#
# Boomer Rehfield - 7/8/2015 
# test
#########################################################################

import os, re
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import LinuxServer
import utilities

django.setup()


def update_server():

    server_list = LinuxServer.objects.filter(decommissioned=False,vmware_cluster='Physical')
    #server_list = LinuxServer.objects.filter(decommissioned=False,name='pinfhdp18')
    number_of_servers = 0
    total = 0
    problem_list = []
    command = 'dzdo cat /proc/cpuinfo | grep processor | wc -l'

    print "Total number of CPUs for all physical servers"

    for server in server_list:
        number_of_servers += 1

        if utilities.ping(server):
            
            client = SSHClient()
            if utilities.ssh(server, client):
                
                print "====================="
                print server.name 
                number_of_server = number_of_servers + 1
                stdin, stdout, stderr = client.exec_command(command)

                try:
                    number = stdout.readlines()[0].rstrip()
                except:
                    number = 'Error'
                    problem_list.append(server.name)
                    continue
                print "CPUs - " + number 
                total = total + int(number)

                #check existing value, if it exists, don't update
                if str(number) != str(server.cpu):
                    utilities.log_change(str(server), 'CPU', str(server.cpu), str(number))
#
                    LinuxServer.objects.filter(name=server).update(cpu=number, modified=timezone.now())
                client.close()

    print "Total CPUs = " + str(total)
    print "Total Servers = " + str(number_of_servers)
    print "Problem Servers = " + str(problem_list)

#start execution
if __name__ == '__main__':
    print "Checking Python versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

