#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to get centrify version
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
from server.models import AIXServer, LinuxServer

from itertools import chain

import utilities
django.setup()



def update_server():
    run_time=str(timezone.now())
    aix_server_list = AIXServer.objects.filter(decommissioned=False, zone=2)
    linux_server_list = LinuxServer.objects.filter(decommissioned=False, zone=2)

    server_list = list(chain(aix_server_list, linux_server_list))

    aix_servers_no_ping = []
    linux_servers_no_ping = []
   
    aix_servers_no_ssh = []
    linux_servers_no_ssh = []

    total_count = 0

    for server in server_list:
        
        total_count = total_count + 1

        if utilities.ping(server):
            
            client = SSHClient()
            if utilities.ssh(server, client):
                new_output = ''

                stdin, stdout, stderr = client.exec_command('dzdo cat /etc/passwd')

                output = stdout.readlines()
                counter1 = 0
                for line in output:
                    counter1 += 1
                    line = line.rstrip()
                    line = str(server) + ":" + line + '\n'
                    new_output += line
                    #print line
                new_output = new_output[:-1]
                if server.os == 'AIX':
                    AIXServer.objects.filter(name=server).update(local_users=new_output)
                else:
                    LinuxServer.objects.filter(name=server).update(local_users=new_output)

                print new_output

            else:
                if server.os == 'AIX':
                    aix_servers_no_ssh.append(server.name)
                else:
                    linux_servers_no_ssh.append(server.name)
        else:
            if server.os == 'AIX':
                aix_servers_no_ping.append(server.name)
            else:
                linux_servers_no_ping.append(server.name)

    print ''
    print "Total count:" + str(total_count)
    print "AIX servers no ping:" + str(aix_servers_no_ping)
    print "Linux servers no ping:" + str(linux_servers_no_ping)
    print "AIX servers no ssh:" + str(aix_servers_no_ping)
    print "Linux servers no ssh:" + str(linux_servers_no_ping)

                #if it's the same version, we don't need to update the record
                #if str(user_count) != str(server.centrify_user_count):

                #CentrifyUserCountAIX.objects.create(run_time=run_time, name=server, user_count=user_count)

                #utilities.log_change(server, 'Centrify user count', str(server.centrify_user_count), str(user_coutn))

                            
                        


#start execution
if __name__ == '__main__':
    print "Checking centrify version..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    from server.models import AIXServer
    update_server()
    elapsed_time= timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
