#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve rsyslog versions and drop them into Django
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
from server.models import AIXServer
import utilities
django.setup()


def update_server():

    #server_list = AIXServer.objects.all()
    server_list = AIXServer.objects.filter(decommissioned=False, active=True)
    #server_list = AIXServer.objects.filter(name='t8sandbox')

    counter = 0

    for server in server_list:
        #counter += 1
        #print str(counter) + ' - ' + str(server)

        if utilities.ping(server):

            client = SSHClient()
            if utilities.ssh(server, client):

                print "---------------------------------"
                print server.name
                #get rsyslog version now
                command = 'lslpp -l | grep rsyslog | uniq'
                stdin, stdout, stderr = client.exec_command(command)
                try:
                    rsyslog_version = stdout.readlines()[0].rstrip()
                    rsyslog_version = rsyslog_version.split()[0] + "." + rsyslog_version.split()[1]
                    print "rsyslog: " + rsyslog_version
                except:
                    rsyslog_version = "None"
                    print "rsyslog: " + rsyslog_version
                

                #check existing value, if it exists, don't update
                #if str(syslog_version) != str(server.syslog):
                #    utilities.log_change(str(server), 'samba', str(server.syslog), str(syslog_version))
                #    AIXServer.objects.filter(name=server).update(syslog=syslog_version, modified=timezone.now())
                if str(rsyslog_version) != str(server.rsyslog):
                    utilities.log_change(str(server), 'rsyslog', str(server.rsyslog), str(rsyslog_version))
                    AIXServer.objects.filter(name=server).update(rsyslog=rsyslog_version, modified=timezone.now())


                
                #command = 'smbd -V'
                #stdin, stdout, stderr = client.exec_command(command)
                #bash_version = stdout.readlines()[0].rstrip()
                #print smbd
                

#start execution
if __name__ == '__main__':
    print "Checking rsyslog versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

