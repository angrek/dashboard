#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve netbackup version and drop them into Django dashboard
#
# Boomer Rehfield - 11/18//2014
#
#########################################################################

import os
from ssh import SSHClient
from django.utils import timezone
from django.contrib.admin.models import LogEntry
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer
import re
import test_server
django.setup()


def update_server():
    server_list = AIXServer.objects.all()
    #server_list = AIXServer.objects.filter(name='u3midcap2')

    for server in server_list:
        server_is_active=1
        if AIXServer.objects.filter(name=server):

            if test_server.ping(server):

                client = SSHClient()
                if test_server.ssh(server, client):

                    stdin, stdout, stderr = client.exec_command('[ -f /usr/openv/netbackup/bin/version ] && cat /usr/openv/netbackup/bin/version || echo "None"')
                    netbackup_version = stdout.readlines()[0]

                    #check existing value, if it exists, don't update
                    if str(netbackup_version) != str(server.netbackup):
                        AIXServer.objects.filter(name=server).update(netbackup=netbackup_version, modified=timezone.now())
                        change_message = 'Changed netbackup to ' + str(netbackup_version)
                        LogEntry.objects.create(action_time='2014-08-25 20:00:00', user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)




#start execution
if __name__ == '__main__':
    print "Checking Netbackup versions..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
