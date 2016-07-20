#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to install centrify direct control
#
# Boomer Rehfield - 6/25/2015
#
#########################################################################

import os
from paramiko import SSHClient

# these are need in django 1.7 and needed vs the django settings command
from django.utils import timezone
import django

from server.models import LinuxServer
import utilities
django.setup()


def update_server():

    # server_list = LinuxServer.objects.filter(zone=1, active=True, exception=False, decommissioned=False).exclude(centrify='5.2.2-192')
    # server_list = LinuxServer.objects.filter(zone=1, active=True, exception=False, decommissioned=False, centrify='5.0.2-388')
    server_list = LinuxServer.objects.filter(zone=1, active=True, decommissioned=False)

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
                old_version = server.centrify
                if server.centrify != '5.3.0-213':

                    print "Checking adquery before install"
                    command = "dzdo adquery user | wc -l"
                    stdin, stdout, stderr = client.exec_command(command)
                    x = stdout.readlines()
                    for line in x:
                        before = line

                    print 'Shutting down direct audit'
                    command = 'dzdo /usr/sbin/dacontrol -d -a'
                    stdin, stdout, stderr = client.exec_command(command)
                    x = stdout.readlines()
                    y = stderr.readlines()
                    for line in x:
                        print line
                    for line in y:
                        print line

                    print 'Creating directory /centrify_install'
                    command = 'dzdo mkdir /centrify_install'
                    stdin, stdout, stderr = client.exec_command(command)
                    x = stdout.readlines()
                    y = stderr.readlines()
                    for line in x:
                        print line
                    for line in y:
                        print line

                    print 'Mounting naswin1 /centrify_install'
                    command = 'dzdo mount -o nolock naswin1:/unix /centrify_install'
                    stdin, stdout, stderr = client.exec_command(command)
                    x = stdout.readlines()
                    y = stderr.readlines()
                    for line in x:
                        print line
                    for line in y:
                        print line

                    print 'Installing centrify'
                    command = "dzdo rpm --force -Uvh /centrify_install/software/Centrify/Centrify-Suite-2016-agents/rhel/centrifydc-5.3.0-rhel4-x86_64.rpm"
                    stdin, stdout, stderr = client.exec_command(command)
                    x = stdout.readlines()
                    y = stderr.readlines()
                    print '3'
                    for line in x:
                        print line
                    for line in y:
                        print line

                    command = 'dzdo /sbin/service centrifydc restart;dzdo /sbin/service sshd restart;dzdo /usr/sbin/adflush -f;dzdo umount /centrify_install;dzdo rmdir /centrify_install'
                    stdin, stdout, stderr = client.exec_command(command)
                    x = stdout.readlines()
                    y = stderr.readlines()
                    for line in x:
                        print line
                    for line in y:
                        print line

                    if server.zone == 2:
                        print 'Enabling direct audit'
                        command = 'dzdo /usr/sbin/dacontrol -e'
                        stdin, stdout, stderr = client.exec_command(command)
                        x = stdout.readlines()
                        y = stderr.readlines()
                        for line in x:
                            print line
                        for line in y:
                            print line

                    print "Old version: " + old_version
                    command = 'adinfo -v'
                    stdin, stdout, stderr = client.exec_command(command)
                    new_centrify = stdout.readlines()[0]
                    new_centrify = new_centrify[19:-2]
                    print "New Version: " + new_centrify

                    print ''
                    print "================================="

                    #Let's update Lizardfish version for the server and log the change
                    server.centrify = new_centrify
                    server.save()
                    utilities.log_change(server, 'Centrify', old_version, new_centrify)

                    # verify
                    print 'Checking adquery after install'
                    command = 'dzdo adquery user | wc -l'
                    stdin, stdout, stderr = client.exec_command(command)
                    x = stdout.readlines()
                    for line in x:
                        after = line
                    print server.name
                    print "==============================="
                    print "users before: " + before.rstrip()
                    print "users after : " + after.rstrip()

            else:
                print "No ssh"
        else:
            print "No ping"


if __name__ == '__main__':
    print "Installing Centrify Direct Control 2016....."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
