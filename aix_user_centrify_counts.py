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
from server.models import AIXServer
from server.models import CentrifyUserCountAIX
from server.models import CentrifyUserCountLinux
from multiprocessing import Pool
import utilities
django.setup()



def update_server(server):

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

                        


if __name__ == '__main__':
    print "Checking centrify version..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = AIXServer.objects.filter(decommissioned=False).exclude(name__contains='vio')
    pool = Pool(30)
    pool.map(update_server, server_list)

    elapsed_time= timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
