#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve OS levels and drop them into Django dashboard
#
# Boomer Rehfield - 8/7/2014
#
#########################################################################

import os
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer
import test_server
import dashboard_logging
django.setup()


def update_server():
    server_list = AIXServer.objects.all()
    #server_list = AIXServer.objects.filter(name='d2vio01')
    #server_list = AIXServer.objects.filter(name__contains='vio')

    for server in server_list:
        
        if test_server.ping(server):

            client = SSHClient()
            if test_server.ssh(server, client):

                #with the vio servers we want the ios.level rather than the os_level
                vio_servers = AIXServer.objects.filter(name__contains='vio')
                if server in vio_servers:
                    command = 'cat /usr/ios/cli/ios.level'
                else:
                    command = 'oslevel -s'
                stdin, stdout, stderr = client.exec_command(command)

                #need rstrip() because there are extra characters at the end
                oslevel = stdout.readlines()[0].rstrip()
                
                #check existing value, if it exists, don't update
                if str(oslevel) != str(server.os_level):
                    dashboard_logging.log_change(str(server), 'oslevel', str(server.os_level), str(oslevel))
                    AIXServer.objects.filter(name=server, exception=False, active=True).update(os_level=oslevel, modified=timezone.now())



#start execution
if __name__ == '__main__':
    print "Checking OS versions..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
