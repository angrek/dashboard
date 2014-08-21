#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Django server database population script - just random info for testing
#
# Boomer Rehfield - 8/7/2014
#
#########################################################################

import os

#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
django.setup()

#FIXME - ok, this is where we need to hit the servers and get what servers actually exist
#server_list = ['d1nim', 'u2jdpdb', 'u3webdb', 'u3jdpdb']

filename = 'ALL_AIX.072114.list.orig'

server_list = open(filename, "r").read().split()

#server_list = fo.readlines()


#starting with AIX servers first
def populate():
    exclusion_list = ['p1vio01', 'p1vio02', 'd1vio01', 'd1vio02', 't1sandbox', 'p3vio01', 'p3vio02', 'd2vio01', 'd2vio02', 'd1sasemin-10152013', 'u3midcap2', 'qpar1midtier', 'p1hmc']
    for server in server_list:
        #get_or_create - no need to check for server first
        if server not in exclusion_list:
            add_server(name=server, os="AIX")

def add_server(name, os):
    s = Server.objects.get_or_create(name=name, os=os)[0]
    return s



#start execution
if __name__ == '__main__':
    print "Starting populations..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    from server.models import Server
    populate()
