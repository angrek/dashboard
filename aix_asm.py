#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to check if powerHA is installed
#
# Boomer Rehfield - 2/3/2015
#
#########################################################################

import os, re
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer
import utilities

django.setup()


def update_server():

    server_list = AIXServer.objects.filter(decommissioned=False)

    counter = 0
    for server in server_list:

        if utilities.ping(server):
            
            client = SSHClient()
            if utilities.ssh(server, client):
                my_output = False
                command = 'lspv | grep ASM | uniq'
                stdin, stdout, stderr = client.exec_command(command)
                output = stdout.readlines()
                for line in output:
                    line = line.rstrip()
                    if re.search("ASM", line):
                        my_output = True


                print '--------'
                print server
                print '111111111111111111111111111'
                print  output
                print '222222222222222222222222222222'
                print  my_output
                print '333333333333333333333333333333'
                print server.asm

                #check existing value, if it exists, don't update
                if my_output != server.asm:
                    utilities.log_change(str(server), 'asm', str(server.asm), str(my_output))

                    AIXServer.objects.filter(name=server).update(asm=my_output, modified=timezone.now())



#start execution
if __name__ == '__main__':
    print "Checking for PowerHA services..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

