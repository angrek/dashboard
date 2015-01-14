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
import utilities
from django.utils import timezone
from subprocess import call, check_output


from django.contrib.admin.models import LogEntry

#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer, Zone, Frame, Stack, Relationships
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

    #temp_frames = ['795A-9119-FHB-SN023D965']

    for frame in frames:
        #the output is throwing newlines at the end of the names for some reason
        #hence the use of rstrip below

        #If the frame doesn't exist, create it
        Frame.objects.get_or_create(name=frame.rstrip())
        frame = Frame.objects.get(name=frame.rstrip())

        #load ssh keys
        #client = paramiko.SSHClient()
        client = SSHClient()
        client.load_system_host_keys()


        #we've already established a connection, but should put in error checking
        #FIXME needs error checking
        client.connect('p1hmc', username="wrehfiel", password=password)

        #for each frame, let's grab the LPARS now
        command = 'lssyscfg -m ' + str(frame) + ' -r lpar -F name'
        #print command
        sdtin, stdout, stderr = client.exec_command(command)
        server_list = stdout.readlines()
        client.close()
        
        counter = 0

        for server_name in server_list:
            #FIXME server is being stupid and just not responding and it's causing an ssh auth error somehow renaming the key, needs error checking!
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

            zone = Zone.objects.get(name='Unsure')


            try:
                server = AIXServer.objects.get(name=server_name.rstrip())
                if server.frame != frame:
                    AIXserver.objects.filter(name=server_name.rstrip()).update(frame=frame)
            except:
                #the created object is not the same, so we create it and then get the instance
                server = AIXServer.objects.get_or_create(name=str(server_name).rstrip(), frame=frame, ip_address=ip_address, os='AIX', zone=zone, active=True, exception=False,  stack_id=1)
                server = AIXServer.objects.get(name=server_name.rstrip())
                change_message = "Added LPAR " + server_name.rstrip() + "."
                LogEntry.objects.create(action_time=timezone.now(), user_id=11 ,content_type_id=9, object_id =264, object_repr=server, action_flag=1, change_message=change_message)
            

            if utilities.ping(server):

                print "ping good" 
                client2 = SSHClient()


                if utilities.ssh(server, client2):
                    #Check for wpars here
                    print "Check for wpars here"
                    command = "dzdo lswpar | grep -v WPAR | grep -v -"
                    stdin, stdout, stderr = client2.exec_command(command)
                    print server
                    #print 'stdout - ' + str(stdout)
                    #FIXME we can do an 'if stderr' mail ....
                    #print 'stderr - ' + str(stderr)
                    for line in stderr:
                        print line
                    #wpar_list = stdout.readlines()[0].rstrip()
                    wpar_list = stdout.readlines()
                    if wpar_list:
                        print '-------------------'
                        for wpar in wpar_list:
                            t= wpar.split()
                            wpar_name = t[3].rstrip()
                            print wpar_name
                            
                            ns_command = 'nslookup ' + wpar_name + ' | grep Address | grep -v "#" '

                            try:
                                ip_address = check_output(ns_command, shell=True)
                                ip_address = ip_address[9:].rstrip()
                            except:
                                ip_address = '0.0.0.0'


                            #We have all of our information for the wpar, let's put it in the database
                            try:
                                temp = AIXServer.objects.get(name=wpar_name)
                            except:

                                #Here we are inheriting some of the parent LPAR objects into the WPAR
                                temp = AIXServer.objects.get_or_create(name=wpar_name, owner=server.owner, frame=server.frame, ip_address=ip_address, os='AIX', zone=server.zone, active=True, exception=False,  stack=server.stack)
                                change_message = "Added WPAR " + wpar_name + "."
                                LogEntry.objects.create(action_time=timezone.now(), user_id=11 ,content_type_id=9, object_id =264, object_repr=server, action_flag=1, change_message=change_message)

                            #Now we'll try and check if the LPAR<->WPAR relationship exists, or create it
                            try:
                                Relationships.objects.get(parent_lpar=server_name, child_wpar=wpar_name)
                            except:
                                child_wpar = AIXServer.objects.get(name=wpar_name)
                                Relationships.objects.get_or_create(parent_lpar=server, child_wpar=child_wpar)
                            

                            
                    else:
                        print "No wpars."

                            
                client2.close()




#start execution
if __name__ == '__main__':
    print "Starting populations..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    populate()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)




