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
from django.utils import timezone
from django.contrib.admin.models import LogEntry

#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer
import ping_server
import logging
django.setup()

logging.basicConfig( level=logging.INFO )

def populate():

    f = open("../../.ssh/p", "r")

    #need rstrip to strip off the newline at the end
    password = str(f.read().rstrip())
    f.close()
    #do I need a ping test for p1hmc?? lol
    client = SSHClient()
    client.load_system_host_keys()
    
    #we don't have ssh keys to p1hmc so this is going to prompt us for a password for now
    try:
        client.connect('p1hmc', username="wrehfiel", password=password)
    except:
        print 'SSH to p1hmc has failed!'

    stdin, stdout, stderr = client.exec_command('lssyscfg -r sys -F name')
    #frames = stdout.readlines()[0]
    frames = stdout.readlines()
    for frame in frames:
        #the output is throwing newlines at the end of the names for some reason
        #hence the use of rstrip below
        #print frame.rstrip()

        client = SSHClient()
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
        for server in server_list:
            print frame.rstrip() + ' -> ' + server.rstrip()
            #quick ping test
            response = ping_server.ping(server)
            #typically 0 = False, but not for ping apparently
            if response == 0:
                #server is active, let's ssh to it
                client = SSHClient()
                client.load_system_host_keys()
                server_is_active=1
                try:
                    client.connect(str(server).rstrip(), username="wrehfiel")

                except:
                    #can't log in, set it as an exception
                    #b = AIXServer(name=server.rstrip(), frame=frame.rstrip(), os='AIX', exception=True)[0]
                    b = AIXServer(name=server.rstrip(), frame=frame.rstrip(), os='AIX', exception=True)
                    b.save()
                    server_is_active=0
                client.close()
                if server_is_active:
                    #server is good, let's add it to the database.
                    #add_server(name=server.rstrip(), frame=frame.rstrip()( os="AIX")
                    b = AIXServer(name=server.rstrip(), frame=frame.rstrip(), os='AIX', exception=False)
                    b.save()


            else:
                #server is inactive, let's flag it
                b = AIXServer(name=server.rstrip(), frame=frame.rstrip(), os='AIX', active=False)
                b.save()



    #for server in exclusion_list:
    #    Server.objects.filter(name=server).update(exception=True)
def add_server(name, frame, os):
    s = Server.objects.get_or_create(name=name, fos='AIX')[0]
    return s



#start execution
if __name__ == '__main__':
    print "Starting populations..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    populate()
