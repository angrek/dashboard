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
import utilities
django.setup()
import paramiko
import getpass
import argparse
import textwrap
from subprocess import *
import sys

#command line arguments and usage
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\

    Set your SSH keys across active AIX and UNIX servers.

    You must use either the --aix or --linux arguments, or both.

    Example:
    ./ssh_keys.py --aix all                   #All AIX servers
    ./ssh_keys.py --aix server1               #One to many servers here
    ./ssh_keys.py --linux all                 #All Linux servers
    ./ssh_keys.py --linux 'server1, server2'  #One to many servers.
                                              #NOTE apostrophes enclose multiple servers.
    ./ssh_keys.py --linux all --aix server1   #You can mix the lists
    ./ssh_keys.py --linux all --aix all       #Transfer keys to all of the servers

    Note: If you wish this to run automatically without being prompted for a
    password, you can put your password into a file named 'p' in
    /home/username/.ssh/p     Lock this file down to 700 permissions.
    '''))

parser.add_argument('--aix', help="Only transfer SSH keys to AIX servers.")
parser.add_argument('--linux', help="Only transfer SSH keys to Linux servers.")
args = parser.parse_args()

#must specify arguments
if not args.aix and args.aix:
    print ''
    parser.print_help()
    sys.exit()


#this will get the username of the person logged in and then prompt them for their password
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
    print args.aix
    print args.linux
    server_list = []

    #Because exceptions are set based on my username running the scripts
    #If another person uses this, his key may be bad even through the
    #exception is False
    if username == 'wrehfiel':
        exception = True
    else:
        exception = False
    #Parse the arguments and create a merge server list
    if args.aix:
        print "aix is a go"
        if args.aix == 'all':
            print 'All'
            server_list += AIXServer.objects.filter(active=True, exception=True, decommissioned=False)
            print server_list
        else:
            for server in [args.aix]:
                server_list += AIXServer.objects.filter(name=server)
            print server_list
           
    if args.linux:
        print 'linux is a go'
        if args.linux == 'all':
            print 'Linux All'
            server_list += LinuxServer.objects.filter(active=True, exception=True, decommissioned=False)
            print server_list
        else:
            for server in [args.linux]:
                server_list += LinuxServer.objects.filter(name=server)
            print server_list
           
    #sys.exit()
    counter = 0
    total = len(server_list)
    for server in server_list:
        server_is_active = 1

        counter = counter + 1
        print 'Working on server ' + str(counter) + "/" + str(total) + " - " + str(server)
            
        if utilities.ping(server):
            print "-Ping test is good"

            all_ahead_flank = 0

            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                client.connect(str(server), username=username, password=password)
            except:
                print 'SSH HAS FAILED'
                print 'Removing key from known_hosts'
                known_hosts = '/home/' + username + '/.ssh/known_hosts'
                file = open(known_hosts)
                lines = file.readlines()
                file.close
                #now reopen it in write mode
                file = open(known_hosts, "w")
                for line in lines:
                    if re.search(server.name, line):
                        print "Found name " + server.name + " entry."
                        file.write(line)
                    if re.search(server.ip_address, line):
                        print "Found IP " + server.ip_address + " entry."
                        file.write(line)
                file.close()
                print 'Trying SSH again'
                #Now lets try to use SSH again
                client = paramiko.SSHClient()
                client.load_system_host_keys()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                print server.ip_address
                #FIXME the below box still isn't working??
                try:
                    client.connect(str(server), username=username, password=password)
                    print "Ok, removing the entry worked."
                except:
                    "SSH STILL NOT WORKING!!!!!!!!!!!!!!!!!!!!!!"
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
                command = '[ -e /home/' + username + '/.ssh/authorized_keys ] || [-e /home/' + username + '/.ssh/authorized_keys2 ] && echo 1 || echo 0'
                print command
                sdtin, stdout, stderr = client.exec_command(command)
                #print stdout.readlines()[0].rstrip()
                if  stdout.readlines()[0].rstrip() == 1:
                    print '-Authorized keys file exists'
                    continue
                else:
                    print '-Authorized keys file does not exist'
                    all_ahead_flank = 1

                client.close()

            if all_ahead_flank:
                print '-Transferring key'
                #now we sftp our key over
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
