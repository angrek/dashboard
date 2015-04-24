#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script check if rsyslog has a bad string and if logging is screwed up
#
# Boomer Rehfield - 4/23/2014
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
    server_list = LinuxServer.objects.filter(decommissioned=False, active=True, exception=False)
    #server_list = LinuxServer.objects.filter(name='dstsmesbapp03')

    counter = 0
    for server in server_list:

        if utilities.ping(server):

            client = SSHClient()
            if utilities.ssh(server, client):
                command = 'ls -lh /var/log/messages'
                stdin, stdout, stderr = client.exec_command(command)
                output = stdout.readlines()
                for line in output:
                    line = line.split()[4]
                #if line.rstrip() == 'rsyslogd is stopped':

                if line == '0':
                    print '================================================'
                    print server.name
                    print line
                    print "RHEL" + str(server.os_level)
                    counter += 1
                    command = 'cat /etc/rsyslog.conf | grep syslog.wellcare.com'
                    stdin, stdout, stderr = client.exec_command(command)
                    output = stdout.readlines()
                    for line in output:
                        print line
                    #LinuxServer.objects.filter(name=server.name).update(rsyslog_r=0, modified=timezone.now())
                    #print 'rsyslog is stopped'
                    #else:
                    #    LinuxServer.objects.filter(name=server.name).update(rsyslog_r=1, modified=timezone.now())
                    #    print 'rsyslog is running'

    print "=============================="
    print "Total server issue count: " + str(counter)

#start execution
if __name__ == '__main__':
    print "Checking for rsyslog issues..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

