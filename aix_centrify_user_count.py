#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to get centrify version
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
from server.models import AIXServer, CentrifyUserCountAIX, CentrifyUserCountLinux

import utilities
django.setup()



def update_server():
    run_time=str(timezone.now())
    server_list = AIXServer.objects.filter(decommissioned=False, active=True, exception=False).exclude(name__contains='vio')

    for server in server_list:

        if utilities.ping(server):
            
            client = SSHClient()
            if utilities.ssh(server, client):


                stdin, stdout, stderr = client.exec_command('adquery user | wc -l')

                user_count = int(stdout.readlines()[0].rstrip())

                print server.name
                print user_count
                #if it's the same version, we don't need to update the record
                #if str(user_count) != str(server.centrify_user_count):

                CentrifyUserCountAIX.objects.create(run_time=run_time, name=server, user_count=user_count)

                #utilities.log_change(str(server), 'Centrify user count', str(server.centrify_user_count), str(user_coutn))

                            
                        


#start execution
if __name__ == '__main__':
    print "Checking centrify version..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    from server.models import AIXServer
    update_server()
    elapsed_time= timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
