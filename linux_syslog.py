#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve syslog and rsyslog versions and drop them into Django
#
# Boomer Rehfield - 2/25/2014
#
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

    #server_list = LinuxServer.objects.all()
    #server_list = LinuxServer.objects.filter(decommissioned=False)
    server_list = LinuxServer.objects.filter(name='ustsesbdb')

    counter = 0

    for server in server_list:
        #counter += 1
        #print str(counter) + ' - ' + str(server)

        if utilities.ping(server):

            client = SSHClient()
            if utilities.ssh(server, client):
                #get syslog version first
                print '------------------------------------'
                print server.name
                command = 'rpm -qa | grep sysklog | uniq'
                stdin, stdout, stderr = client.exec_command(command)
                try:
                    syslog_version = stdout.readlines()[0].rstrip()
                    print syslog_version 
                except:
                    syslog_version = "None"
                    print syslog_version
                
                #get rsyslog version now
                command = 'rpm -qa | grep rsyslog | uniq'
                stdin, stdout, stderr = client.exec_command(command)
                try:
                    rsyslog_version = stdout.readlines()[0].rstrip()
                    print rsyslog_version 
                except:
                    rsyslog_version = "None"
                    print rsyslog_version
                

                #check existing value, if it exists, don't update
                if str(syslog_version) != str(server.syslog):
                    utilities.log_change(str(server), 'syslog', str(server.syslog), str(syslog_version))
                    LinuxServer.objects.filter(name=server).update(syslog=syslog_version, modified=timezone.now())
                if str(rsyslog_version) != str(server.rsyslog):
                    utilities.log_change(str(server), 'rsyslog', str(server.rsyslog), str(rsyslog_version))
                    LinuxServer.objects.filter(name=server).update(rsyslog=rsyslog_version, modified=timezone.now())


                
                #command = 'smbd -V'
                #stdin, stdout, stderr = client.exec_command(command)
                #bash_version = stdout.readlines()[0].rstrip()
                #print smbd
                

#start execution
if __name__ == '__main__':
    print "Checking Bash versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

