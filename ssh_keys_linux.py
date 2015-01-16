#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to set up SSH keys on the linux servers
#
# Boomer Rehfield - 8/7/2014
#
#########################################################################

import os
import re
from ssh import SSHClient
from django.utils import timezone
from server.models import AIXServer, LinuxServer

#need itertools to concatenate the query sets to combine lists of servers from two different tables
from itertools import chain

#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
import utilities
django.setup()
import paramiko
import getpass

#this will get the username of the person logged in and then prompt them for their password
username = getpass.getuser()
print "You are logged in as " + username
if username == 'wrehfie':
    f = open("/home/wrehfiel/.ssh/p", "r")
    password = str(f.read().rstrip())
    f.close
else:
    password = getpass.getpass()

def update_server():
    counter = 0
    server_list = LinuxServer.objects.filter(active=True, decommissioned=False)

    for server in server_list:
        server_is_active = 1

        counter = counter + 1
        print 'Working on server ' + str(counter) + " - " + str(server)
            
        if utilities.ping(server):
            print "-Ping test is good"

            all_ahead_flank = 0

            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                client.connect(str(server), username=username, password=password, timeout=7)
            except:
                print 'SSH HAS FAILED. BREAKING LOOP HERE'
                continue
            command = '[ -d /home/' + username + '/.ssh ] && echo 1 || echo 0'
            #command = 'ls /home'
            sdtin, stdout, stderr = client.exec_command(command)
            directory_exists = stdout.readlines()
            client.close()
            #print "stdout!"
            #print directory_exists[0].rstrip()
            if directory_exists[0].rstrip() == '0':
                print '-Ssh directory does not exist. Creating'
                #directory does not exist so we need to create it
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
                client.connect(str(server), username=username, password=password, allow_agent=True, look_for_keys=True, timeout=7)
                command = 'mkdir /home/' + username + '/.ssh;chmod 700 /home/' + username + '/.ssh'
                sdtin, stdout, stderr = client.exec_command(command)
                #dont' think I really need to grab stdout here
                #test = stdout.readlines()
                client.close()
                all_ahead_flank = 1
                print '-Directory created'
            else:
                print '-Checking for authorized_keys'
                #if the directory exists, test if authorized_keys exists
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
                client.connect(str(server), username=username, password=password, timeout=7)
                command = '[ -e /home/' + username + '/.ssh/authorized_keys ] || [-e /home' + username + '/.ssh/authorized_keys2 ] && echo 1 || echo 0'
                sdtin, stdout, stderr = client.exec_command(command)
                if stdout.readlines()[0].rstrip():
                    print '-Authorized keys file exists'
                    continue
                else:
                    print '-Authorized keys file does NOT exist'
                    all_ahead_flank = 1

                client.close()
                
            if all_ahead_flank:
                print '-Transferring key'
                #now we sftp our key over
                transport = paramiko.Transport((str(server), 22))

                try:
                    transport.connect(username=username, password=password)
                except:
                    #FIXME if the try isn't working, thisi isn't getting printed out
                    continue

                sftp = paramiko.SFTPClient.from_transport(transport)
                local = '/home/' + username + '/.ssh/id_rsa.pub'
                remote = '/home/' + username + '/.ssh/authorized_keys'
                sftp.put(remote, local)
                sftp.close()
                transport.close()
                
                #we've transferred it, but we need to rename the file now
                #the paramiko sftp won't rename it (or I haven't figured it out yet -Boomer)
                client.connect(str(server), username=username, password=password, timeout=7)
                command = 'mv /home/' + username + '/.ssh/id_rsa.pub /home/' + username + '/.ssh/authorized_keys'
                sdtin, stdout, stderr = client.exec_command(command)
                print '-Key transferred and renamed'
                client.close()
        else:
                print '-Server is unreachable by ping!!!!!!!!!!'





#start execution
if __name__ == '__main__':
    print "Beginning your SSH key transfers..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
