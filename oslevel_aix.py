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
from server.models import Server
django.setup()


def update_server():
    server_list = Server.objects.all()
    for server in server_list:
        client = SSHClient()
        client.load_system_host_keys()
        client.connect(str(server), username="wrehfiel")
        stdin, stdout, stderr = client.exec_command('oslevel -s')
        oslevel = stdout.readlines()[0]
        Server.objects.filter(name=server, exception=False, active=True).update(os_level=oslevel)
        Server.objects.filter(name=server, exception=False, active=True).update(modified=timezone.now())



#start execution
if __name__ == '__main__':
    print "Checking OS versions..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
