#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve syslog and rsyslog versions and drop them into Django
#
# Boomer Rehfield - 2/25/2014
#
#########################################################################

import os
from ssh import SSHClient

# these are need in django 1.7 and needed vs the django settings command
from django.utils import timezone
import django

from server.models import LinuxServer
import utilities
django.setup()


def update_server():

    # server_list = LinuxServer.objects.filter(zone=1, active=True, exception=False, decommissioned=False).exclude(centrify='5.2.2-192')
    server_list = LinuxServer.objects.filter(name__contains='pdlpap04')

    for server in server_list:

        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        print server.name

        if utilities.ping(server):

            client = SSHClient()

            if utilities.ssh(server, client):
                print "Current centrify version:"
                print server.centrify
                # FIXME  #FIXME #FIXME
                if server.centrify != '5.2.2-1922':

                    print 'Creating directory /centrify_install'
                    command = 'dzdo mkdir /centrify_install'
                    stdin, stdout, stderr = client.exec_command(command)
                    x = stdout.readlines()
                    y = stderr.readlines()
                    print x
                    for line in x:
                        print line
                    for line in y:
                        print line

                    print 'Mounting naswin1 /centrify_install'
                    command = 'dzdo mount -o nolock naswin1:/unix /centrify_install'
                    stdin, stdout, stderr = client.exec_command(command)
                    x = stdout.readlines()
                    y = stderr.readlines()
                    print '2'
                    for line in x:
                        print line
                    for line in y:
                        print line

                    print 'Installing centrifyda'
                    command = 'dzdo rpm -Uvh /centrify_install/software/Centrify/Centrify-Suite-2015-agents-DM/centrify-suite-2015-5.2.2-192/rhel/centrifyda-3.2.2-rhel3-x86_64.rpm'
                    stdin, stdout, stderr = client.exec_command(command)
                    x = stdout.readlines()
                    y = stderr.readlines()
                    print '3'
                    for line in x:
                        print line
                    for line in y:
                        print line

                    command = 'dzdo service centrifyda restart;dzdo adreload;dzdo umount /centrify_install;dzdo rmdir /centrify_install'
                    stdin, stdout, stderr = client.exec_command(command)
                    x = stdout.readlines()
                    for line in x:
                        print line

                    command = 'dzdo rpm -qa | grep entrify'
                    stdin, stdout, stderr = client.exec_command(command)
                    x = stdout.readlines()
                    for line in x:
                        print line

            else:
                print "No ssh"
        else:
            print "No ping"

            # t = stdout.readlines()
            # for line in t:
            #    print line.rstrip()
            #
            # print '---------------------------'

            # command = 'cat /etc/rsyslog.conf'
            # stdin, stdout, stderr = client.exec_command(command)

            # try changing chkconfig
            # command = 'chkconfig --list | grep rsyslog'
            # stdin, stdout, stderr = client.exec_command(command)
            # t = stdout.readlines()[0]
            # print t


if __name__ == '__main__':
    print "Checking and installing rsyslog."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
