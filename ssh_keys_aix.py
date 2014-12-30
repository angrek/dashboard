#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve SSL versions on the servers and drop them into Django dashboard
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
import test_server
django.setup()
import paramiko
import getpass

#this will get the username of the person logged in and then prompt them for their password
username = getpass.getuser()
print "You are logged in as " + username
password = getpass.getpass()

def update_server():
    counter = 0
    #server_list = AIXServer.objects.all()
    #the below exception is for my account's inability to ssh in (service account in the future)
    #Part 2 - revisiting what is or isn't an exception later, might be changing the field
    #server_list_aix = AIXServer.objects.filter(active=True)
    #server_list = AIXServer.objects.filter(active=True, exception=True).exclude(name='t8sandbox')
    #server_list = AIXServer.objects.filter(active=True)
    server_list = AIXServer.objects.filter(name='p1fwadb')
    #server_list_linux = LinuxServer.objects.filter(active=True)
    #server_list = list(chain(server_list_aix, server_list_linux))

    for server in server_list:
        server_is_active = 1

        #FIXME just remove this, this was just so I knew how much longer it was running
        counter = counter + 1
        print 'Working on server ' + str(counter) + " - " + str(server)
        #removed exception because it should be an exception (should it filter exception=True???)
        if AIXServer.objects.filter(name=server):
            
            if test_server.ping(server):
                print "-Ping test is good"

                all_ahead_flank = 0

                client = paramiko.SSHClient()
                client.load_system_host_keys()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    client.connect(str(server), username=username, password=password)
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
                    client.connect(str(server), username=username, password=password, allow_agent=True, look_for_keys=True)
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
                    client.connect(str(server), username=username, password=password)
                    command = '[ -e /home/' + username + '/.ssh/authorized_keys ] && echo 1 || echo 0'
                    sdtin, stdout, stderr = client.exec_command(command)
                    #dont' think I really need to grab stdout here
                    key_file_exists = stdout.readlines()
                    #print key_file_exists[0].rstrip()
                    client.close()
                    if key_file_exists[0].rstrip() == '0':
                        print '-Authorized keys file does not exist'
                        all_ahead_flank = 1
                    else:
                        print '-Authorized keys file does exist'
                    
                #print 'all ahead flank?' + str(all_ahead_flank)
                if all_ahead_flank:
                    print '-Transferring key'
                    #now we ftp our key over
                    transport = paramiko.Transport((str(server), 22))
                    #just testing why it's not getting here...
                    #transport.load_system_host_keys()
                    #transport.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    transport.connect(username = username , password=password)

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
                    print '-Key transferred and renamed'
                    client.close()
                else:
                    print '-Key already exists, you should be good to go!'
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
