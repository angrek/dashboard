#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve syslog and rsyslog versions and drop them into Django
#
# Boomer Rehfield - 2/25/2014
#
#########################################################################

import os, re, time
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import LinuxServer
import utilities
django.setup()
import paramiko
import getpass

def update_server():
    username = getpass.getuser()
    path = '/home/' + username + '/.ssh/p'
    f = open(path, "r")
    password = str(f.read().rstrip())
    f.close
    #server_list = LinuxServer.objects.all()
    #zone = NonProduction = 1
    server_list = LinuxServer.objects.filter(zone=2, decommissioned=False, rsyslog_r=0)
    #server_list = LinuxServer.objects.filter(name='b1esbapp')

    counter = 0

    for server in server_list:
        #counter += 1
        #print str(counter) + ' - ' + str(server)
        if server.rsyslog is not 'None':
            if utilities.ping(server):

                client = SSHClient()
                if utilities.ssh(server, client):
                    #if rsyslogd is running, it's not one of our installs
                    #and we don't want to overwrite the rsyslog.conf in
                    #case it has been previously modified
                    command = 'dzdo /sbin/service rsyslog status'
                    stdin, stdout, stderr = client.exec_command(command)
                    output = stdout.readlines()
                    for line in output[:1]:

                        if line.rstrip() == 'rsyslogd is stopped':

                            #get syslog version first
                            print '------------------------------------'
                            print 'Rsyslog is stopped on ' + server.name
                            print "Current rsyslog version:"
                            print server.rsyslog

                            #check chkconfig
                            command = 'dzdo /sbin/chkconfig --list | grep syslog'
                            stdin, stdout, stderr = client.exec_command(command)
                            output = stdout.readlines()
                            for line in output:
                                print line

                            print '----'
                            
                            rsyslog_header = ['# Use traditional timestamp format',
                            '$ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat',
                            '',
                            '# Provides kernel logging support (previously done by rklogd)',
                            '$ModLoad imklog',
                            '# Provides support for local system logging (e.g. via logger command)',
                            '$ModLoad imuxsock']

                            os.system('>/tmp/rsyslog.conf')
                           
                            
                            transport = paramiko.Transport((str(server), 22))
                            try:
                                transport.connect(username = username, password = password)
                            except:
                                "Something went wrong with the SFTP connection"
                                continue
                            sftp = paramiko.SFTPClient.from_transport(transport)
                            local = '/tmp/syslog.conf'
                            remote = '/etc/syslog.conf'
                            sftp.get(remote, local)

                            with open('/tmp/syslog.conf') as f1:
                                with open('/tmp/rsyslog.conf', 'w') as f2:
                                    for line in rsyslog_header:
                                        f2.write(line)
                                    for line in f1:
                                        f2.write(line)


                            local = '/tmp/rsyslog.conf'
                            remote = '/tmp/rsyslog.conf'
                            sftp.put(local, remote)

                            sftp.close()
                            transport.close()

                            #command = 'ls -l /tmp/*syslog.conf'
                            #stdin, stdout, stderr = client.exec_command(command)
                            #output = stdout.readlines()
                            #for line in output:
                            #    print line

                            #can't sftp the file over as root, so we need to copy it over
                            #and set permissions
                            command = 'dzdo mv /tmp/rsyslog.conf /etc/rsyslog.conf'
                            stdin, stdout, stderr = client.exec_command(command)
                            time.sleep(2)
                            command = 'dzdo chmod 644 /etc/rsyslog.conf'
                            stdin, stdout, stderr = client.exec_command(command)
                            time.sleep(2)
                            command = 'dzdo chown root:root /etc/rsyslog.conf'
                            stdin, stdout, stderr = client.exec_command(command)

                            #script is running too fast and the sleeps are needed
                            time.sleep(2)

                            #double check the permissions
                            print 'checking permissions'
                            command = 'ls -l /etc/*syslog.conf'
                            stdin, stdout, stderr = client.exec_command(command)
                            output = stdout.readlines()
                            for line in output:
                                print line



                            #turn on rsyslog and turn off syslog
                            command = 'dzdo /sbin/chkconfig rsyslog on'
                            stdin, stdout, stderr = client.exec_command(command)


                            command = 'dzdo /sbin/chkconfig syslog off'
                            stdin, stdout, stderr = client.exec_command(command)

                            command = '/sbin/chkconfig --list | grep syslog'
                            stdin, stdout, stderr = client.exec_command(command)
                            output = stdout.readlines()
                            for line in output:
                                print line

                            print 'Stopping syslog'
                            command = 'dzdo /sbin/service syslog stop'
                            stdin, stdout, stderr = client.exec_command(command)

                            time.sleep(2)
                            command = 'dzdo /sbin/service rsyslog start'
                            stdin, stdout, stderr = client.exec_command(command)

                            time.sleep(2)
                            command = 'dzdo /sbin/service syslog status'
                            stdin, stdout, stderr = client.exec_command(command)
                            output = stdout.readlines()
                            for line in output:
                                print line
                            command = 'dzdo /sbin/service rsyslog status'
                            stdin, stdout, stderr = client.exec_command(command)
                            output = stdout.readlines()
                            for line in output:
                                print line

                            LinuxServer.objects.filter(name=server).update(rsyslog_r=1, modified=timezone.now())
                        else:
                            print "Rsyslog is running on " + server.name + ", moving on to the next server."








                

#start execution
if __name__ == '__main__':
    print "Checking and installing rsyslog."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

