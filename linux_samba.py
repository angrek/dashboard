#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve samba versions and drop them into Django dashboard
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

    server_list = LinuxServer.objects.all()
    #server_list = LinuxServer.objects.filter(decommissioned=False)
    #server_list = LinuxServer.objects.filter(name='uprspegaapp01')

    counter = 0

    for server in server_list:
        #counter += 1
        #print str(counter) + ' - ' + str(server)

        if utilities.ping(server):

            client = SSHClient()
            if utilities.ssh(server, client):
                print '------------------------------------'
                print server.name
                command = '/usr/sbin/smbd -V'
                #command = 'dzdo smbd -V'
                stdin, stdout, stderr = client.exec_command(command)
                try:
                    samba = stdout.readlines()[0]
                    print samba 
                except:
                    samba = "None"
                    print samba
                
                #bash_version = re.sub(r'x86_64', '', bash_version)

                #check existing value, if it exists, don't update
                if str(samba) != str(server.samba):
                    utilities.log_change(str(server), 'samba', str(server.samba), str(samba))
                    LinuxServer.objects.filter(name=server, exception=False, active=True).update(samba=samba, modified=timezone.now())

                
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

