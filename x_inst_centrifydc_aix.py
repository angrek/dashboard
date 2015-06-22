#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to upgrade to the new centrify patch
#
# Boomer Rehfield - 5/19/2014
#
#########################################################################

import os, re, time
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer
import utilities
django.setup()


def update_server():

    #server_list = AIXServer.objects.filter(name__contains='uhdpdb01', zone=1, active=True, exception=False, decommissioned=False).exclude(centrify='5.2.2-192')
    server_list = AIXServer.objects.filter(zone=2, name__contains='p1sasgrid01', decommissioned=False).exclude(centrify='5.2.2-192', name__contains='vio')
    #server_list = AIXServer.objects.filter(name__contains='uinfmsdb01')

    counter = 0

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

                if server.centrify != '5.2.2-192':

                    print 'Checking adquery before install'
                    command = 'dzdo adquery user | wc -l'
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



                    print 'Creating directory /unix_centrify'
                    command = 'dzdo mkdir /unix_centrify'
                    stdin, stdout, stderr = client.exec_command(command)
                    x = stdout.readlines()
                    y = stderr.readlines()
                    print x
                    for line in x:
                        print line
                    for line in y:
                        print line


                    print 'Mounting naswin1 /unix_centrify'
                    command = 'dzdo mount naswin1:/unix /unix_centrify'
                    stdin, stdout, stderr = client.exec_command(command)
                    x = stdout.readlines()
                    y = stderr.readlines()
                    print '2'
                    for line in x:
                        print line
                    for line in y:
                        print line

                    print 'Installing centrify'
                    #command = 'dzdo installp -acFY -d /unix_centrify/software/Centrify/Centrify-Suite-2015-agents-DM/centrify-suite-2015-5.2.2-192/aix_install CentrifyDC.core;sleep 7;dzdo adflush -a;dzdo adreload;sleep 2'
                    command = 'dzdo installp -acFY -d /unix_centrify/software/Centrify/Centrify-Suite-2015-agents-DM/centrify-suite-2015-5.2.2-192/aix/ CentrifyDC.core;sleep 7;dzdo adflush -a;dzdo adreload;sleep 2'
                    stdin, stdout, stderr = client.exec_command(command)
                    x = stdout.readlines()
                    y = stderr.readlines()
                    print '3'
                    #for line in x:
                    #    print line
                    #for line in y:
                    #    print line



                    print 'Unmounting naswin1 /unix_centrify'
                    command = 'dzdo umount /unix_centrify'
                    stdin, stdout, stderr = client.exec_command(command)

                    print 'Removing directory /unix_centrify'
                    command = 'dzdo rmdir /unix_centrify'
                    stdin, stdout, stderr = client.exec_command(command)


                    #verify
                    print 'Checking adquery after install'
                    command = 'dzdo adquery user | wc -l'
                    stdin, stdout, stderr = client.exec_command(command)
                    x = stdout.readlines()
                    for line in x:
                        after = line
                    print server.name    
                    print "===============================" 
                    print "Users before: " + before.rstrip()
                    print "Users after : " + after.rstrip()



                    #This is a line in case I have issues and need to start killing
                    # a hung centrifydc process
                    if int(after.rstrip()) == 0:
                        print "*************************************************"
                        print "CENTRIFY IS HANGING!!!!"
                        print "*************************************************"
                    #ps ef | grep centrifydc | awk '{print $2}' | xargs kill -9
                    #startsrc -s centrifydc




                    #print "Stopping Centrify"
                    #command = 'dzdo stopsrc -s centrifydc;sleep 5'
                    #stdin, stdout, stderr = client.exec_command(command)
                    #x = stdout.readlines()
                    #for line in x:
                    #    print line
                    #y = stderr.readlines()
                    #for line in y:
                    #    print line

                    #command = "dzdo ssh " + str(server.name) + " startsrc -s centrifydc"
                    #os.system(command)
                    #print "Waiting 10 seconds"
                    #time.sleep(10)

                    #print "Starting centrify"
                    #command = 'dzdo startsrc -s centrifydc;dzdo adflush -f'
                    #stdin, stdout, stderr = client.exec_command(command)
                    #x = stdout.readlines()
                    #for line in x:
                    #    print line
                    #y = stderr.readlines()
                    #for line in y:
                    #    print line

                    print 'Enabling direct audit'
                    command = 'dzdo /usr/sbin/dacontrol -e -a'
                    stdin, stdout, stderr = client.exec_command(command)
                    x = stdout.readlines()
                    y = stderr.readlines()
                    for line in x:
                        print line
                    for line in y:
                        print line



                    print "Old Version: " + old_version
                    command = 'adinfo -v'
                    stdin, stdout, stderr = client.exec_command(command)
                    new_centrify = stdout.readlines()[0]
                    new_centrify = new_centrify[19:-2]
                    print "New Version: " + new_centrify

                    print ''
                    print "================================="

                    server.centrify = new_centrify
                    server.save()
                    utilities.log_change(str(server), 'Centrify', old_version, new_centrify)

            else:
                print "No ssh"
        else:
            print "No ping"

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

