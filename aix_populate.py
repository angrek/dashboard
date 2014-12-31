#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Django server database population script
# This will
#   -Go to the HMC and pull all frames
#   -Read all Lpar names from each frame
#   -test to see if it is active
#   -test ssh connectivity
#   -check for wpars
#   -check each wpars status and ssh connectivity
#   -update the server database accordingly for each step
#
# Boomer Rehfield - 8/7/2014
#
#########################################################################

import os
from ssh import SSHClient
#import paramiko
import test_server
from django.utils import timezone
from subprocess import call, check_output


from django.contrib.admin.models import LogEntry

#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer, Zone, Frame
#import logging
django.setup()

#logging.basicConfig( level=logging.INFO )

def populate():

    f = open("../../.ssh/p", "r")

    #need rstrip to strip off the newline at the end
    password = str(f.read().rstrip())
    f.close()
    #do I need a ping test for p1hmc?? lol
    client = SSHClient()
    client.load_system_host_keys()
    
    try:
        client.connect('p1hmc', username="wrehfiel", password=password)
    except:
        print 'SSH to p1hmc has failed!'
        print '*************HAVE YOU CHANGED YOUR PASSWORD RECENTLY??***********'
    stdin, stdout, stderr = client.exec_command('lssyscfg -r sys -F name')
    #frames = stdout.readlines()[0]
    frames = stdout.readlines()
    for frame in frames:
        #the output is throwing newlines at the end of the names for some reason
        #hence the use of rstrip below
        #print frame.rstrip()

        #If the frame doesn't exist, create it
        Frame.objects.get_or_create(name=frame.rstrip())
        frame = Frame.objects.get(name=frame.rstrip())

        #load ssh keys
        #client = paramiko.SSHClient()
        client = SSHClient()
        client.load_system_host_keys()


        #we've already established a connection, but should put in error checking
        #FIXME
        client.connect('p1hmc', username="wrehfiel", password=password)

        #for each frame, let's grab the LPARS now
        command = 'lssyscfg -m ' + str(frame) + ' -r lpar -F name'
        #print command
        sdtin, stdout, stderr = client.exec_command(command)
        server_list = stdout.readlines()
        client.close()
        
        counter = 0

        #server_list2 = ('upar2diamdb', 'upar2cesdb01', 'upar2midtier')
        for server_name in server_list:
            print server_name
            update = 0
            counter += 1
            #for troubleshooting - please leave
            #print str(counter) + " - " + frame + ' -> ' + server.rstrip()


            #Before we ping and do our other tests we're going to get the ip address from
            #nslookup. If this fails it will simply return a blank.
             
            ns_command = 'nslookup ' + server_name.rstrip() + ' | grep Address | grep -v "#" '
            try:
                ip_address = check_output(ns_command, shell=True)
                ip_address = ip_address[9:]
            except:
                ip_address = '0.0.0.0'

            #FIXME - apparently without the rstrip, it adds /n to the end, which
            #screws up our silencing of the ping and creates stdout ping response
            #to be printed.... what the hell man.... not really a FIXME, more of an FYI :\
            #server = server.rstrip()
            zone = Zone.objects.get(name='Unsure')


            try:
                server = AIXServer.objects.get(name=server_name.rstrip())
            except:
                #the created object is not the same, so we create it and then get the instance
                server = AIXServer.objects.get_or_create(name=str(server_name).rstrip(), frame=frame, ip_address=ip_address, os='AIX', zone=zone, active=True, exception=False,  stack_id=1)
                server = AIXServer.objects.get(name=server_name.rstrip())
            

            if test_server.ping(server):

                print "ping good" 
                client2 = SSHClient()


                if test_server.ssh(server, client2):
                    #Check for wpars here
                    print "Check for wpars here"

                client2.close()




#start execution
if __name__ == '__main__':
    print "Starting populations..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    populate()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)




