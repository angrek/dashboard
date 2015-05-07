#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve syslog and rsyslog versions and drop them into Django
#
# Boomer Rehfield - 2/25/2014
#
#########################################################################

import os, re, time
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import LinuxServer
import utilities
django.setup()


def update_server():

    #server_list = LinuxServer.objects.filter(active=True, exception=False, zone=1, decommissioned=False).exclude(centrify='5.2.2-192')
    server_list = LinuxServer.objects.filter(name='trh1sandbox')

    counter = 0

    for server in server_list[:25]:

        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        print server.name

        if utilities.ping(server):

            client = SSHClient()
            if utilities.ssh(server, client):
                print "Current centrify version:"
                print server.centrify

                #command = 'cat /etc/syslog.conf'
                #stdin, stdout, stderr = client.exec_command(command)
                #t = stdout.readlines()
                #for line in t:
                #    print line.rstrip()
#
 #               print '---------------------------'

                #command = 'cat /etc/rsyslog.conf'
                #stdin, stdout, stderr = client.exec_command(command)

                #try changing chkconfig
                #command = 'chkconfig --list | grep rsyslog'
                #stdin, stdout, stderr = client.exec_command(command)
                #t = stdout.readlines()[0]
                #print t


            

#start execution
if __name__ == '__main__':
    print "Checking and installing rsyslog."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

