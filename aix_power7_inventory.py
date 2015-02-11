#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Django, AIX Power7 inventory scripts. This is for gathering the mem
#   and cpu stats right now from the HMC and drop it into Django.
#
# Ok, for now this may be called from main script (future plans)
# but the idea is that the server and frame checks will have already
# been done so if it's pulling it from the frame, then it should already
# be in the database. I 'think' get_or_create should work here fine..
# Testing for now....
#
# Boomer Rehfield - 9/22/2014
#
#########################################################################

import os, sys
from ssh import SSHClient
from django.utils import timezone
from django.contrib.admin.models import LogEntry

#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer, Power7Inventory
import logging
django.setup()

logging.basicConfig( level=logging.INFO )

def populate():

    f = open("../../.ssh/p", "r")

    #need rstrip to strip off the newline at the end
    password = str(f.read().rstrip())
    f.close()
    client = SSHClient()
    client.load_system_host_keys()
    
    try:
        client.connect('phmc01', username="wrehfiel", password=password)
    except:
        print 'SSH to phmc01 has failed!'
        sys.exit()

    #Grab all of the frames on the HMC
    stdin, stdout, stderr = client.exec_command('lssyscfg -r sys -F name')

    frames = stdout.readlines()
    for frame in frames:
        #the output is throwing newlines at the end of the names for some reason
        #hence the use of rstrip below
        #print frame.rstrip()

        client = SSHClient()
        client.load_system_host_keys()

        #we've already established a connect6ion, but should put in error checking
        #FIXME
        client.connect('phmc01', username="wrehfiel", password=password)

        types = ['proc', 'mem']

        for type in types:
            #for each frame, let's get all of the HMC memory data
            command = 'lshwres -r ' + type + ' -m ' + frame.rstrip() + ' --level lpar'
            print command

            stdin, stdout, stderr = client.exec_command(command)
            lpar_list = stdout.readlines()
            #we'll close the connection after the next section

            lpar_array = {}
            for lpar in lpar_list:
                lpar_dict = lpar.split(",")
                for entry in lpar_dict:
                    #test for an empty value
                    if entry:
                        a,b = entry.split('=')
                        lpar_array[a] = b

                #ok, first we want to get the lpar name and then remove it from the dict
                #NOTE: in the database it is FK to 'name'. When I created the server db
                #I just called it name so that's why there is a difference. I can't go back
                #and change it because it is populated with WPARs also.
                server_name = lpar_array['lpar_name']
                print server_name
                #deleting so we can iterate over all of the values
                del lpar_array['lpar_name']
               
                #in case the server is new since the last time it ran, we'll just create a blank server record and then update it.
                #we don't really need error checking here because it's whatever the HMC gave us and the previous scripts will have added them to the AIXServer database.
                name = AIXServer.objects.get(name=server_name)
                print name
                Power7Inventory.objects.get_or_create(name=name, frame=name.frame, active=name.active, exception=name.exception, decommissioned=name.decommissioned)
                for key, value in lpar_array.iteritems():
                    print key, "=>",value
                    print "attempting to update value...."
                    Power7Inventory.objects.filter(name=name).update(**{key: value})

###########temp comment block
        #for each frame, let's get all of the HMC CPU data for it
#        command = 'lshwres -r mem -m ' + frame.rstrip() + ' --level lpar'
#        print command
#
#        sdtin, stdout, stderr = client.exec_command(command)
#        lpar_list = stdout.readlines()
#        client.close()
#
#        lpar_array = {}
#        for lpar in lpar_list:
#            print ">>>>>>>> " + lpar
#            print " "
#            lpar_dict = lpar.split(",")
#            for entry in lpar_dict:
#                #test for an empty value
#                if entry:
#                    a,b = entry.split('=')
#                    lpar_array[a] = b
#        
#        for name, possible_items in lpar_array.iteritems():
#            print name, "=>",possible_items 
##############

        #Ok, here's the break in logic from the others. We don't need to hit the servers.
        #For each frame, run the lshwres command and that will spit out the data for
        #all of its LPARs. For each row, split by comma, and then by equal sign and
        #drop into an array.



#        for server in server_list:
#            print frame.rstrip() + ' -> ' + server.rstrip()
#            #quick ping test
#            response = ping_server.ping(server)
#            #typically 0 = False, but not for ping apparently
#            if response == 0:
#                #server is active, let's ssh to it
#                client = SSHClient()
#                client.load_system_host_keys()
#                server_is_active=1
#                try:
#                    client.connect(str(server).rstrip(), username="wrehfiel")
#
#                except:
#                    #can't log in, set it as an exception
#                    #b = AIXServer(name=server.rstrip(), frame=frame.rstrip(), os='AIX', exception=True)[0]
#                    try:
#                        AIXServer.objects.filter(name=server.rstrip()).update(frame=frame.rstrip(), os='AIX', exception=True, modified=timezone.now())
#                        change_message = "Could not SSH to server. Set exception to True"
#                        #LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)
#                    except:
##                        AIXServer.objects.get_or_create(name=server.rstrip(), frame=frame.rstrip(), os='AIX', exception=True)
#                    server_is_active=0
#                client.close()
#                if server_is_active:
#                    #server is good, let's add it to the database.
#                    #add_server(name=server.rstrip(), frame=frame.rstrip()( os="AIX")
#                    try:
#                        AIXServer.objects.filter(name=server.rstrip()).update(frame = frame.rstrip(), os='AIX', exception=False, modified=timezone.now())
#                    except:
#                        AIXServer.objects.get_or_create(name=server.rstrip(), frame=frame.rstrip(), os='AIX', exception=False)
#
#
#            else:
#                #server is inactive, let's flag it
#                try:
#                    AIXServer.objects.filter(name=server.rstrip()).update(frame=frame.rstrip(), os='AIX', active=False, modified=timezone.now())
#                    change_message = "Server is now inactive. Set active to False"
#                    #LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)
#                except:
#                    AIXServer.objects.get_or_create(name=server.rstrip(), frame=frame.rstrip(), os='AIX', active=False)



    #for server in exclusion_list:
    #    Server.objects.filter(name=server).update(exception=True)
#def add_server(name, frame, os):
#    s = Server.objects.get_or_create(name=name, fos='AIX')[0]
#    return s



#start execution
if __name__ == '__main__':
    print "Starting populations..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    populate()
