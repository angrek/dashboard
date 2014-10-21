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
import ping_server
from django.utils import timezone
from subprocess import call, check_output


from django.contrib.admin.models import LogEntry

#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer, Zone
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

        client = paramiko.SSHClient()
        client.load_system_host_keys()

        #we've already established a connect6ion, but should put in error checking
        #FIXME
        client.connect('p1hmc', username="wrehfiel", password=password)

        #for each frame, let's grab the LPARS now
        command = 'lssyscfg -m ' + frame.rstrip() + ' -r lpar -F name'
        #print command
        sdtin, stdout, stderr = client.exec_command(command)
        server_list = stdout.readlines()
        client.close()
        
        counter = 0

        for server in server_list:
            counter += 1
            print str(counter) + " - " + frame.rstrip() + ' -> ' + server.rstrip()


            #Before we ping and do our other tests we're going to get the ip address from
            #nslookup. If this fails it will simply return a blank.
             
            ns_command = 'nslookup ' + server.rstrip() + ' | grep Address | grep -v "#" '
            try:
                ip_address = check_output(ns_command, shell=True)
                ip_address = ip_address[9:]
            except:
                ip_address = '0.0.0.0'

            #quick ping test
            #FIXME - apparently without the rstrip, it adds /n to the end, which
            #screws up our silencing of the ping and creates stdout ping response
            #to be printed.... what the hell man....
            server = server.rstrip()
            response = ping_server.ping(server)

            if response == 0:
                print "-Ping test is good"
                #server is active, let's ssh to it
                client = paramiko.SSHClient()
                client.load_system_host_keys()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                server_is_active=1
                try:
                    client.connect(str(server).rstrip(), username="wrehfiel", password=password)
                except:
                    ####can't log in, set it as an exception
                    #b = AIXServer(name=server.rstrip(), frame=frame.rstrip(), os='AIX', exception=True)[0]
                    try:
                        AIXServer.objects.get(name=server.rstrip())
                        #print '11111111111111111111'
                        AIXServer.objects.filter(name=server.rstrip()).update(frame=frame.rstrip(), ip_address=ip_address, os='AIX', exception=True, modified=timezone.now())
                        change_message = "Could not SSH to server. Set exception to True"
                        #LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)
                    except:
                        zone = Zone.objects.get(name='Unsure')
                        AIXServer.objects.get_or_create(name=server.rstrip(), frame=frame.rstrip(), ip_address=ip_address, os='AIX', zone=zone, exception=True)
                        #print '22222222222222222222222222222'
                    server_is_active=0
                client.close()
                if server_is_active:
                    #server is good, let's add it to the database.
                    #add_server(name=server.rstrip(), frame=frame.rstrip()( os="AIX")
                    try:
                        AIXServer.objects.get(name=server.rstrip())
                        #print '333333333333333333333333'
                        #FIXME why am I setting the os if I am just updating??
                        AIXServer.objects.filter(name=server.rstrip()).update(frame = frame.rstrip(), ip_address=ip_address, os='AIX', exception=False, modified=timezone.now())
                    except:
                        #print '4444444444444444444444444444444'
                        zone = Zone.objects.get(name='Unsure')
                        AIXServer.objects.get_or_create(name=server.rstrip(), frame=frame.rstrip(), ip_address=ip_address, os='AIX', zone=zone, exception=False)



            else:
                #server is inactive, let's flag it
                try:
                    print '55555555555555555555555555555555'
                    AIXServer.objects.get(name=server.rstrip())
                    #print '5555555555555555555555555555'
                    AIXServer.objects.filter(name=server.rstrip()).update(frame=frame.rstrip(), ip_address=ip_address, os='AIX', active=False, modified=timezone.now())
                    change_message = "Server is now inactive. Set active to False"
                    #LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)
                except:
                    print '666666666666666666666666666'
                    zone = Zone.objects.get(name='Unsure')
                    AIXServer.objects.get_or_create(name=server.rstrip(), frame=frame.rstrip(), ip_address=ip_address, os='AIX', zone=zone, active=False)



    #for server in exclusion_list:
    #    Server.objects.filter(name=server).update(exception=True)
def add_server(name, frame, os):
    s = Server.objects.get_or_create(name=name, fos='AIX')[0]
    return s



#start execution
if __name__ == '__main__':
    print "Starting populations..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    populate()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)




