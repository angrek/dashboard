#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# This is to pull data from Django and drop it into Excel for
# capacity planning
#
# Boomer Rehfield - 10/22/2014
#
#########################################################################

import os
import re
from ssh import SSHClient
import paramiko
from django.utils import timezone
from server.models import AIXServer, Power7Inventory

#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
django.setup()

import ping_server


def get_server_data():
    counter = 0
    #server_list = AIXServer.objects.all()
    #shortening this just to speed up testing
    server_list = AIXServer.objects.filter(name__contains='vio')
    for server in server_list:

        #FIXME just remove this, this was just so I knew how much longer it was running
        counter = counter + 1
        r = Power7Inventory.objects.get(name=server)
        t = AIXServer.objects.get(name=server)
        print str(counter) + ',' + str(server) + ',AIX,VM,' + t.ip_address.rstrip() + ',,,,' + str(r.curr_procs)
        #AIXServer.objects.filter(name=server).update(active=False, modified=timezone.now())
        #print str(server) + ' not responding to ping, setting to inactive.'
        #LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='Ping failed, changed to inactive.')




#start execution
if __name__ == '__main__':
    print "Getting server information..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    get_server_data()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
