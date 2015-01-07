#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve Linux OS levels and drop them into Django dashboard
#
# Boomer Rehfield - 11/13/2014
#
#########################################################################

import os
import re
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import LinuxServer
import test_server
import dashboard_logging
django.setup()


def update_server():
    #server_list = LinuxServer.objects.all()
    server_list = LinuxServer.objects.filter(decommissioned=False)
    #server_list = LinuxServer.objects.filter(name='d0mwcdb')

    for server in server_list:

        if test_server.ping(server):

            client = SSHClient()
            if test_server.ssh(server, client):

                command = 'lsb_release -a | grep Distributor'
                stdin, stdout, stderr = client.exec_command(command)

                #need rstrip() because there are extra characters at the end
                os = stdout.readlines()[0].rstrip()
                os = re.sub('Distributor ID:', '', os)
                os = re.sub('\s*', '', os)


                if os == 'RedHatEnterpriseServer':
                    os = 'RHEL'
                else:
                    os = 'Unknown'


                command = 'lsb_release -a | grep Release'
                stdin, stdout, stderr = client.exec_command(command)

                oslevel = stdout.readlines()[0].rstrip()
                oslevel = re.sub('Release:', '', oslevel)
                oslevel = re.sub('\s*', '', oslevel)

                #check existing value, if it exists, don't update
                if str(os) != str(server.os):
                    dashboard_logging.log_change(str(server), 'OS', str(server.os), str(os))
                    LinuxServer.objects.filter(name=server, exception=False, active=True).update(os=os, modified=timezone.now())
                if str(oslevel) != str(server.os_level):
                    dashboard_logging.log_change(str(server), 'OS Level', str(server.os_level), str(oslevel))
                    LinuxServer.objects.filter(name=server, exception=False, active=True).update(os_level=oslevel, modified=timezone.now())


if __name__ == '__main__':
    print "Checking OS versions..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
