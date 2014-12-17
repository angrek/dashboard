#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to storage size of each of the servers
#
# Boomer Rehfield - 10/24/2014
#
#########################################################################

import os
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer, Storage
import test_server
django.setup()



def update_server():

    #FIXME need to exclude vio servers
    server_list = AIXServer.objects.all().exclude(name__contains='vio')
    #server_list = AIXServer.objects.filter(name__contains='p1vio01')
    #server_list = AIXServer.objects.filter(name__contains='auto').exclude(name__contains='vio')

    counter  = 1
    for server in server_list:

            
        if test_server.ping(server):

            client = SSHClient()
            if test_server.ssh(server, client):

                stdin, stdout, stderr = client.exec_command('sudo /scripts/dashboard_disksize.sh')

                for line in stdout:
                    print line.rstrip()
                
                counter += 1
                try:
                    Storage.objects.get(name=server)
                    Storage.objects.filter(name=server).update(size=line.rstrip())
                except:
                    Storage.objects.get_or_create(name=server, size=line.rstrip())



#start execution
if __name__ == '__main__':
    print "Storage size for each server..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    from server.models import AIXServer
    update_server()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
