#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve SSL versions on the servers and drop them into Django dashboard
#
# Boomer Rehfield - 8/7/2014
#
#########################################################################

import os
import re
from ssh import SSHClient
import paramiko
from django.utils import timezone
from django.contrib.admin.models import LogEntry
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
import test_server
django.setup()


def update_server():

    server_list = AIXServer.objects.all()
    #server_list = AIXServer.objects.filter(name__contains='uftsmidtier')
    for server in server_list:

        if test_server.ping(server):

            client = SSHClient()
            if test_server.ssh(server, client):

                stdin, stdout, stderr = client.exec_command('lslpp -l | grep -i openssh.base.server | uniq')
                #this is going to pull 4 different parts of ssl, we just need the base
                rows = stdout.readlines()
                if rows:
                    row = rows[0]
                    #split the lines and grab the first one
                    temp = row.split("\r")[0]
                    p = re.compile(r' +')
                    temp2 = p.split(temp)
                    ssh = temp2[2]

                    #if existing value is the same, don't update
                    if str(ssh) != str(server.aix_ssh):

                        old_version = str(server.aix_ssh)
                        AIXServer.objects.filter(name=server, exception=False, active=True).update(aix_ssh=ssh, modified=timezone.now())
                        change_message = 'Changed AIX SSH version from ' + old_version + ' to ' + str(ssh)
                        LogEntry.objects.create(action_time='2014-08-25 20:00:00', user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)



#start execution
if __name__ == '__main__':
    print "Checking AIX SSH versions..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    from server.models import AIXServer
    update_server()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
