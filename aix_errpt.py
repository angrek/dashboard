#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to get AIX errpts
#
# Boomer Rehfield - 9/5/2014
#
#########################################################################

import os
from ssh import SSHClient
from django.utils import timezone
from django.contrib.admin.models import LogEntry
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer, Errpt
import test_server
django.setup()



def update_server():
    #right now we are just getting these for the VIO servers
    server_list = AIXServer.objects.filter(name__contains='vio')

    for server in server_list:

        if test_server.ping(server):

            client = SSHClient()
            if test_server.ssh(server, client):
                stdin, stdout, stderr = client.exec_command('errpt | tail -n 20"')
                report = ''

                #we have to do errpt differently due to the way it is handled by stdout
                for line in stdout:
                    report = report + str(line)
                if report == '':
                    report = "The errpt was empty."
            
                #we don't care about the old record and we'll just add another
                Errpt.objects.get_or_create(name=server, report=report, modified=timezone.now())
                change_message = 'Updated errpt.'
                LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)




#start execution
if __name__ == '__main__':
    print "Getting Errpts..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    from server.models import AIXServer
    update_server()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
