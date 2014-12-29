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
import paramiko
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
        client = paramiko.SSHClient()
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

        for server_name in server_list:
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

            #quick ping test
            #FIXME - apparently without the rstrip, it adds /n to the end, which
            #screws up our silencing of the ping and creates stdout ping response
            #to be printed.... what the hell man.... not really a FIXME, more of an FYI :\
            #server = server.rstrip()
            zone = Zone.objects.get(name='Unsure')

            #need to convert the server name to a database instance
            try:
                server = AIXServer.objects.get(name=server_name.rstrip())
                update = 1
            except:
                #the created object is not the same, so we create it and then get the instance
                server = AIXServer.objects.get_or_create(name=str(server_name).rstrip(), frame=frame, zone=zone, stack_id=1)
                server = AIXServer.objects.get(name=server_name.rstrip())
            

            if test_server.ping(server):
                server = str(server).rstrip()

                #server is active, let's ssh to it
                client = paramiko.SSHClient()
                client.load_system_host_keys()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_is_good=1
                try:
                    client.connect(str(server).rstrip(), username="wrehfiel", password=password)
                except:
                    ####can't log in, set it as an exception
                    if update:
                        AIXServer.objects.get(name=server.rstrip())
                        AIXServer.objects.filter(name=server.rstrip()).update(frame=frame, ip_address=ip_address, exception=True, modified=timezone.now())
                        change_message = "Could not SSH to server. Set exception to True"
                        #LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)
                    else:
                        zone = Zone.objects.get(name='Unsure')
                        AIXServer.objects.get_or_create(name=str(server).rstrip(), frame=frame, ip_address=ip_address, os='AIX', zone=zone, exception=True, stack_id=1)
                    ssh_is_good = 0
                client.close()

                if ssh_is_good:

                    #server is good, let's add it to the database.
                    if update:
                        AIXServer.objects.get(name=str(server).rstrip())
                        AIXServer.objects.filter(name=str(server).rstrip()).update(frame = frame, ip_address=ip_address, exception=False, modified=timezone.now())

                    else:
                        #print '4444444444444444444444444444444'
                        zone = Zone.objects.get(name='Unsure')
                        AIXServer.objects.get_or_create(name=str(server).rstrip(), frame=frame, ip_address=ip_address, os='AIX', zone=zone, exception=False, stack_id=1)


            else:
                #server is inactive, let's flag it
                if update:
                    AIXServer.objects.get(name=str(server).rstrip())
                    AIXServer.objects.filter(name=str(server).rstrip()).update(frame=frame, ip_address=ip_address, os='AIX', active=False, modified=timezone.now())
                    change_message = "Server is now inactive. Set active to False"
                    #LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)

                else:
                    zone = Zone.objects.get(name='Unsure')
                    AIXServer.objects.get_or_create(name=str(server).rstrip(), frame=frame, ip_address=ip_address, os='AIX', zone=zone, active=False, stack_id=1)





#start execution
if __name__ == '__main__':
    print "Starting populations..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    populate()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)




