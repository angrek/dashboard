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
    text = f.read()
    print text
    f.close()
    #do I need a ping test for p1hmc?? lol
    client = SSHClient()
    client.load_system_host_keys()
    
    #we don't have ssh keys to p1hmc so this is going to prompt us for a password for now
    try:
        client.connect('p1hmc', username="wrehfiel", password='Boomer77')
    except:
        print 'SSH to p1hmc has failed!'

    stdin, stdout, stderr = client.exec_command('lssyscfg -r sys -F name')
    #frames = stdout.readlines()[0]
    frames = stdout.readlines()
    for frame in frames:

        #the output is throwing newlines at the end of the names for some reason
        #hence the use of rstrip below
        print frame.rstrip()
        #for each frame, let's grab the LPARS now
        command = 'lssyscfg -m ' + frame.rstrip() + ' -r lpar -F name'
        #print command
        sdtin, stdout, stderr = client.exec_command(command)
        server_list = stdout.readlines()
        for server in server_list:
            print frame.rstrip() + ' -> ' + server.rstrip()
            #add_server(name=server.rstrip(), frame=frame.rstrip()( os="AIX")
            AIXServer.objects.get_or_create(name=server.rstrip(), frame=frame.rstrip(), os='AIX')[0]

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
