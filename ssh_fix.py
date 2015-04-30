#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to fix my ssh keys
# Works fine on Linux but probs with AIX and it's account locking stuff
#
# Boomer Rehfield - 4/29/2015
#
#########################################################################

import os
import re
from ssh import SSHClient
from django.utils import timezone
from server.models import AIXServer, LinuxServer, Relationships

#need itertools to concatenate the query sets to combine lists of servers from two different tables
from itertools import chain

#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
import utilities
django.setup()
import paramiko
import getpass
import argparse
import textwrap
from subprocess import *
import sys

#this will get the username of the person logged in and then prompt them for their passwor
#unless they have it in a file named p in their .ssh dir. See Usage.
username = getpass.getuser()
print "You are logged in as " + username
command = '[ -e /home/' + username + '/.ssh/p ] && echo 1 || echo 0'

file_exists = int(Popen(command, shell=True, stdout=PIPE).stdout.readlines()[0])
if file_exists:
    path = '/home/' + username + '/.ssh/p'
    f = open(path, "r")
    password = str(f.read().rstrip())
    f.close
else:
    password = getpass.getpass()

def update_server():

    #Get the list of lpars that host wpars
    lpar_list = Relationships.objects.values('parent_lpar').distinct()
    for lpar in lpar_list:
        lpar = lpar['parent_lpar']
        print "====================================================="
        print "Working on lpar host " + lpar

        #First we're just going to adflush the lpar
        #I could just do this as root, but I'd prefer to try it as myself first
        #side note: I ran this with just an ls command to verify/cheat
        #and make sure I could get into them all first
        #If I can't get into the lpar as root, I'm essentially screwed anyway
        #command = "ssh " + lpar + " dzdo adflush -f"
        #print command
        #os.system(command)

    #command = 'dzdo ssh ' + str(server) + ' adflush -f'
    #os.system(command)



    sys.exit()
    #print "Trying to run adflush as root...."
    #command = 'dzdo ssh ' + str(server) + ' adflush -f'
    #os.system(command)
          
    server_list = AIXServer.objects.filter(decommissioned=False, active=True, exception=True)
    for server in server_list2:

        print '--------------------------------------'
        print 'Working on server ' + str(server)
            
        if utilities.ping(server):
            print "Ping test is good"

            keys_file_does_not_exist = 0

            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                client.connect(str(server), username=username, password=password)
                #FIXME if this works, we should continue to the next server, right??
                #there is nothing to do right? or should I be testing with keys not pass??
            except:
                print 'SSH has failed'
                print 'Removing key from known_hosts'
                known_hosts = '/home/' + username + '/.ssh/known_hosts'
                file = open(known_hosts)
                lines = file.readlines()
                file.close()
                #now reopen it in write mode
                file = open(known_hosts, "w")
                for line in lines:
                    if not re.search(server.name, line):
                        file.write(line)
                file.close()

                file = open(known_hosts)
                lines = file.readlines()
                file.close()
                file = open(known_hosts, 'w')

                for line in lines:
                    if not re.search(server.ip_address, line):
                        file.write(line)
                file.close()


                print 'Trying SSH again'
                #Now lets try to use SSH again
                client = paramiko.SSHClient()
                client.load_system_host_keys()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                #FIXME the below box still isn't working??
                try:
                    client.connect(str(server), username=username, password=password)
                    print "Ok, removing the entry worked."
                except:
                    print "SSH STILL NOT WORKING!!!!!!!!!!!!!!!!!!!!!!"
                    print "Trying to run adflush as root...."
                    command = 'dzdo ssh ' + str(server) + ' adflush -f'
                    os.system(command)
                    continue

            command = '[ -d /home/' + username + '/.ssh ] && echo 1 || echo 0'
            #command = 'ls /home'
            sdtin, stdout, stderr = client.exec_command(command)
            directory_exists = stdout.readlines()
            client.close()
            #print "stdout!"
            #print directory_exists[0].rstrip()
            if directory_exists[0].rstrip() == '0':
                print 'SSH directory does not exist. Creating'
                #directory does not exist so we need to create it
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
                client.connect(str(server), username=username, password=password, allow_agent=True, look_for_keys=True)
                command = 'mkdir /home/' + username + '/.ssh;chmod 700 /home/' + username + '/.ssh'
                sdtin, stdout, stderr = client.exec_command(command)
                client.close()

                #directory doesn't exist, so the keys file doesn't either
                keys_file_does_not_exist = 1
                print 'SSH Directory created'
            else:
                print 'SSH directory exists, checking for authorized_keys'
                #if the directory exists, test if authorized_keys exists
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
                client.connect(str(server), username=username, password=password)

                #this is a one off for red hat 6 and selinux, but it needs some testing
                #command = "restorecon -R ~/.ssh"
                #stdin, stdout, stderr = client.exec_command(command)

                command = '[ -e /home/' + username + '/.ssh/authorized_keys ] || [-e /home/' + username + '/.ssh/authorized_keys2 ] && echo 1 || echo 0'
                sdtin, stdout, stderr = client.exec_command(command)

                output = stdout.readlines()[0].rstrip()
                if  output == '1':
                    print output
                    print 'Authorized keys file exists, moving on to the next server.'
                    command = '/sbin/restorecon -R /home/' + username + '/.ssh'
                    stdin, stdout, stderr = client.exec_command(command)
                    continue
                else:
                    print output 
                    print 'Authorized keys file does not exist.'
                    keys_file_does_not_exist = 1

                client.close()

            if keys_file_does_not_exist:
                print 'Transferring key'
                #sftp our key over
                transport = paramiko.Transport((str(server), 22))

                try:
                    transport.connect(username = username , password=password)
                except:
                    #FIXME if the try isn't working, this isn't getting printed out
                    print "Connection is timing out for some reason............"
                    continue

                sftp = paramiko.SFTPClient.from_transport(transport)
                local = '/home/' + username + '/.ssh/id_rsa.pub'
                remote = '/home/' + username + '/.ssh/authorized_keys'
                sftp.put(remote, local)
                sftp.close()
                transport.close()
                
                #we've transferred it, but we need to rename the file now
                #the paramiko sftp won't rename it (or I haven't figured it out yet -Boomer)
                client.connect(str(server), username=username, password=password)
                command = 'mv /home/' + username + '/.ssh/id_rsa.pub /home/' + username + '/.ssh/authorized_keys'
                sdtin, stdout, stderr = client.exec_command(command)
                command = 'chmod 600 /home/' + username + '/.ssh/authorized*'
                sdtin, stdout, stderr = client.exec_command(command)
                print '-Key transferred and renamed'
                command = "dzdo restorecon -R ~/.ssh"
                stdin, stdout, stderr = client.exec_command(command)
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
