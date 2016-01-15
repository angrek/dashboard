#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve OS levels and drop them into Django dashboard
#
# Boomer Rehfield - 8/7/2014
#
#########################################################################

import os
import re
from ssh import SSHClient
import smtplib
from email.mime.text import MIMEText
import email.utils
from django.utils import timezone
#from django.contrib.admin.models import LogEntry
#these are need in django 1.7 and needed vs the django settings command
import django
import utilities
from dashboard import settings
from server.models import AIXServer
from server.models import LinuxServer
django.setup()


def update_server():

    server_list = []
    linux_servers = []
    aix_servers = []

    file = open('/home/wrehfiel/ENV/dashboard/syslogservers', 'r')
    for line in file:
        server_list.append(line.rstrip())

    #FIXME
    for server in server_list:
        rsyslog_flag = 0

        #lets divide the server into two lists first
       
        if AIXServer.objects.filter(name=server).exists():
            try:
                server = AIXServer.objects.filter(name=server)[0]
            except:
                print "Server issue for AIX host " + str(server)
                continue
            aix_servers.append(server)
        else:
            try:
                server = LinuxServer.objects.filter(name=server)[0]
            except:
                print "Server issue for LINUX host " + str(server)
                continue
            linux_servers.append(server)

         
       
        #test a connection
        print "-------------------" + str(server) + "---------------------\n"
        #client = SSHClient()
        #client.load_system_host_keys()
        #client.connect(str(server), username="wrehfiel")

        if utilities.ping(server):

            print "Ping is good"

            client = SSHClient()

            if utilities.ssh(server, client):

                print "SSH is good"

                #is rsyslog running?
                #command = 'dzdo /sbin/service rsyslog status' 
                command = 'dzdo ps -ef | grep syslog | grep -v grep' 
                stdin, stdout, stderr = client.exec_command(command)
                t = stdout.readlines()
                for line in t:
                    if re.search('syslog', line):
                        print line.rstrip()
                        rsyslog_flag = 1 


                    #if yes check for syslog.wellcare.com and remove it
                if rsyslog_flag:
                    command = 'grep syslog.wellcare.com /etc/rsyslog.conf' 
                    stdin, stdout, stderr = client.exec_command(command)
                    s = stdout.readlines()
                    for line in s:
                        if re.search('syslog.wellcare.com', line):
                            print 'there is a syslog.wellcare.com entry'
                            print line.rstrip()



                #if yes check for itsecsyslog

                #if no to itsecsyslog add it

                #restart rsyslog


                #if rsyslog is not running, check for syslog.conf

                #if syslog is running check for syslog.wellcare.com and remove it

                #if syslog is running check for itsecsyslog

                #if itsecsyslog does not exist, add it to the end

                #if flagged for the above, restart syslog

        #command = 'grep syslog.wellcare.com /etc/rsyslog.conf'
        #command = 'cat /etc/rsyslog.conf'
        #stdin, stdout, stderr = client.exec_command(command)
        #for output in stdout.readlines():
        #    print output
    #        text = text + output + '\n'
    #print text


    #TEST LIST OF DIVIDING UP THE SERVERS"
    #print "Linux Servers"
    #print "----------------------------------------"
    #for host in linux_servers:
    #    print host.name
    #print "AIX Servers"
    #print "----------------------------------------"
    #for host in aix_servers:
    #    print host.name





    #message = """From: Boomer <william.rehfield@wellcare.com>
    #To: Boomer <william.rehfield@wellcare.com>
    #Suject: ESB /opt console.log Report.""" + text
    #msg = MIMEText(text)
    #msg['Subject'] = 'ESB /opt console.log report'
    #msg['From'] = email.utils.formataddr(('Boomer', "william.rehfield\@wellcare.com"))
    #msg['To'] = email.utils.formataddr(('Boomer', "william.rehfield\@wellcare.com"))

    #s = smtplib.SMTP('localhost')
    #s.sendmail(

    #server = smtplib.SMTP('mail')
    #server.sendmail("william.rehfield@wellcare.com", "william.rehfield@wellcare.com",msg.as_string())
 


#start execution
if __name__ == '__main__':
    print "Running..."
    #print timezone.now()
    #os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    #print timezone.now()
