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


#Temporary server list
server_list = ['u2jdpdb', 'u3webdb', 'd1nim']



#starting with AIX servers first
#def populate():
#    update_server(name="d1nim", ip_address="10.5.32.72", os="AIX", os_level="7100-03-03-1415")
#    update_server(name="u2jdpdb", ip_address="10.5.44.73", os="AIX", os_level="6100-09-02-1311")
#    update_server(name="u3webdb", ip_address="10.5.45.56", os="AIX", os_level="6100-09-02-1311")


def update_server():
    for name in server_list:
        client = SSHClient()
        client.load_system_host_keys()
        client.connect(name, username="wrehfiel")
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
            Server.objects.filter(name=name, exception=False, active=True).update(ssl=ssl)
            Server.objects.filter(name=name, exception=False, active=True).update(modified=timezone.now())

    #s = Server.objects.get_or_create(name=name, ip_address=ip_address, os=os, os_level=os_level)[0]
    #return s



#start execution
if __name__ == '__main__':
    print "Starting populations..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    from server.models import Server
    update_server()
