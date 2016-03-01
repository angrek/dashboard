#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve bash versions 
#
# Boomer Rehfield - 8/7/2014
# test
#########################################################################

import os
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer
import utilities
from multiprocessing import Pool
django.setup()


def update_server(server):



    if utilities.ping(server):
        
        client = SSHClient()
        if utilities.ssh(server, client):
            print server.name                
            command = 'dzdo rpm -qa | grep bash |grep -v doc'
            stdin, stdout, stderr = client.exec_command(command)
            try:
                bash_version = stdout.readlines()[0].rstrip()
            except:
                print "Problem getting bash version"
                continue
            stdin.close()
            stderr.close()
            
            #check existing value, if it exists, don't update
            if str(bash_version) != str(server.bash):
                utilities.log_change(server, 'bash', str(server.bash), str(bash_version))

                AIXServer.objects.filter(name=server).update(bash=bash_version, modified=timezone.now())
            client.close()



#start execution
if __name__ == '__main__':
    print "Checking Bash versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    
    server_list = AIXServer.objects.filter(decommissioned=False)
    pool = Pool(20)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

