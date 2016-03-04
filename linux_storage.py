#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve bash versions and drop them into Django dashboard
#
# Boomer Rehfield - 11/13/2014
#
#########################################################################

import os, re
from ssh import SSHClient
from django.utils import timezone
from django.contrib.admin.models import LogEntry
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import LinuxServer
import utilities
from multiprocessing import Pool
django.setup()


def update_server(server):


    if utilities.ping(server):

        client = SSHClient()

        if utilities.ssh(server, client): 
            command = 'dzdo /sbin/fdisk -l | grep Disk'
            stdin, stdout, stderr = client.exec_command(command)
            print stdout
            size = stdout.readlines()
            for line in (size):
                print line
            print size
            print 'Size' + str(size[1])
            exit
            continue
            #FIXME above
                             
            bash_version = re.sub(r'x86_64', '', bash_version)

            #check existing value, if it exists, don't update
            if str(bash_version) != str(server.bash):
                LinuxServer.objects.filter(name=server, exception=False, active=True).update(bash=bash_version, modified=timezone.now())
                change_message = 'Changed bash version to ' + str(bash_version)
                LogEntry.objects.create(action_time='2014-08-25 20:00:00', user_id=11, content_type_id=16, object_id=264, object_repr=server, action_flag=2, change_message=change_message)



#start execution
if __name__ == '__main__':
    print "Checking Bash versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = LinuxServer.objects.filter(decommissioned=False)

    pool = Pool(30)
    pool.map(update_server, server_list)

    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

