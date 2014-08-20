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


#Temporary server list
server_list = ['d1nim', 'u2jdpdb', 'u3webdb']




def update_server():
    for name in server_list:
        client = SSHClient()
        client.load_system_host_keys()
        client.connect(name, username="wrehfiel")
        stdin, stdout, stderr = client.exec_command('adinfo -v')
        centrify = stdout.readlines()[0]
        #strings in Python are immutable so we need to create a new one
        new_centrify = centrify[8:-2]
        Server.objects.filter(name=name, exception=False, active=True).update(centrify=new_centrify)
        Server.objects.filter(name=name, exception=False, active=True).update(modified=timezone.now())

    #s = Server.objects.get_or_create(name=name, ip_address=ip_address, os=os, os_level=os_level)[0]
    #return s



#start execution
if __name__ == '__main__':
    print "Starting populations..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    from server.models import Server
    update_server()
