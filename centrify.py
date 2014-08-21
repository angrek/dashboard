#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to get centrify version and drop it into Django dashboard
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
django.setup()


def update_server():
    server_list = Server.objects.all()
    for server in server_list:
        print server.ssl
        client = SSHClient()
        client.load_system_host_keys()
        client.connect(str(server), username="wrehfiel")
        stdin, stdout, stderr = client.exec_command('adinfo -v')
        centrify = stdout.readlines()[0]
        #strings in Python are immutable so we need to create a new one
        new_centrify = centrify[8:-2]
       
        #if it's the same version, we don't need to update the record
        if str(new_centrify) != str(server.centrify):
            Server.objects.filter(name=server, exception=False, active=True).update(centrify=new_centrify)
            Server.objects.filter(name=server, exception=False, active=True).update(modified=timezone.now())




#start execution
if __name__ == '__main__':
    print "Checking centrify version..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    from server.models import Server
    update_server()
