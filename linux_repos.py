#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve bash versions and drop them into Django dashboard
#
# Boomer Rehfield - 11/13/2014
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
import paramiko
django.setup()


def update_server():

    #good_group = []
    epel_group = {}
    extras_group = []
    not_registered_group = []
    bad_group = []

    good_group = {}

    server_list = LinuxServer.objects.filter(decommissioned=False, active=True)
    #server_list = LinuxServer.objects.filter(name='dinfhdp00')

    counter = 0

    for server in server_list[:3]:

        if utilities.ping(server):

            client = paramiko.SSHClient()
            if utilities.ssh(server, client):
                
                print '---------------------------------------------------------------------------------'
                print server.name
                command = ' dzdo yum repolist enabled | grep -v updates | grep -v Loaded | grep -v repolist | grep -v status'
                stdin, stdout, stderr = client.exec_command(command)
              
                epel_flag = 0
                tmp_line = ''
                line_counter = 0
                for line in stdout:
                    tmp_line = tmp_line + line
                    line_counter = line_counter + 1
                    line = line.rstrip()
                    print line.rstrip()
                    #print line_counter

                    if re.search('epel', line):
                        epel_flag = 1

                    if re.search('not registered', line):
                        not_registered_group.append(str(server.name))

                #print "line_counter = " + str(line_counter)
                #print len(str(line_counter))
                if epel_flag:
                    epel_group[str(server.name)] = tmp_line
                    #epel_group.append(str(server.name))

                if str(line_counter) == '1':
                    if re.search('07312015', line):
                        #good_group.append(str(server.name))
                        good_group[str(server.name)] = tmp_line
                    else:
                        bad_group.append(str(server.name))
                        print "Bad line" + line
                else:
                    extras_group.append(str(server.name))

    print '======================================================================================='
    print '======================================================================================='
    print '======================================================================================='
    print 'Good Servers:' 
    
    #print tmp_good_group
    for s,t in good_group.iteritems():
        print '------------------------------'
        print s.rstrip()
        print t.rstrip()

    print '======================================================================================='
    print '======================================================================================='
    print '======================================================================================='
    print 'Servers with EPEL: ' 
    
    for s,t in epel_group.iteritems():
        print '------------------------------'
        print s.rstrip()
        print t.rstrip()

    print '======================================================================================='
    print '======================================================================================='
    print '======================================================================================='
    print 'Servers not registered: ' + str(not_registered_group)
    
    print '======================================================================================='
    print '======================================================================================='
    print '======================================================================================='
    print 'Servers with extra repos: ' + str(extras_group)
    
    print '======================================================================================='
    print '======================================================================================='
    print '======================================================================================='
    print 'Servers with bad repos: ' + str(bad_group)
    


                #check existing value, if it exists, don't update
                #if str(bash_version) != str(server.bash):
                #    utilities.log_change(str(server), 'bash', str(server.bash), str(bash_version))
                #    LinuxServer.objects.filter(name=server, exception=False, active=True).update(bash=bash_version, modified=timezone.now())



#start execution
if __name__ == '__main__':
    print "Checking Bash versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

