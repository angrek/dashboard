#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve OS levels and drop them into Django dashboard
#
# Boomer Rehfield - 8/7/2014
#
#########################################################################

import os
import re
from ssh import SSHClient
from django.utils import timezone

#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
django.setup()


def update_server():
    server_list = Server.objects.all()
    for server in server_list:
        client = SSHClient()
        client.load_system_host_keys()
        client.connect(str(server), username="wrehfiel")
        stdin, stdout, stderr = client.exec_command('lslpp -l | grep -i openssl.base')
        #this is going to pull 4 different parts of ssl, we just need the base
        rows = stdout.readlines()
        if rows:
            row = rows[0]
            #split the lines and grab the first one
            temp = row.split("\r")[0]
            p = re.compile(r' +')
            temp2 = p.split(temp)
            ssl = temp2[2]
            
            #if existing value is the same, don't update
            if str(ssl) != str(server.ssl):
                Server.objects.filter(name=server, exception=False, active=True).update(ssl=ssl)
                Server.objects.filter(name=server, exception=False, active=True).update(modified=timezone.now())



#start execution
if __name__ == '__main__':
    print "Checking SSL versions..."
    print timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    from server.models import Server
    update_server()
    print timezone.now()
