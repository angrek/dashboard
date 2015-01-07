#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to get centrify version from the Linux servers and drop it into Django dashboard
#
# Boomer Rehfield - 11/13/2014
#
#########################################################################

import os
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import LinuxServer, Zone
import test_server
import dashboard_logging
django.setup()



def update_server():
    #server_list = LinuxServer.objects.all()
    server_list = LinuxServer.objects.filter(decommissioned=False)
    #server_list = LinuxServer.objects.filter(name='ustswebdb')

    for server in server_list:

        new_centrify = ''

        if test_server.ping(server):

            client = SSHClient()
            if test_server.ssh(server, client):

                centrify_is_installed = 1
                stdin, stdout, stderr = client.exec_command('adinfo -v')
                try:
                    centrify = stdout.readlines()[0]
                    new_centrify = centrify[19:-2]
                except:
                    new_centrify = "Not Installed"
                    centrify_is_installed = 0

                #if it's the same version, we don't need to update the record
                if str(new_centrify) != str(server.centrify):
                    dashboard_logging.log_change(str(server), 'Centrify', str(server.centrify), str(new_centrify))
                    LinuxServer.objects.filter(name=server, exception=False, active=True).update(centrify=new_centrify, modified=timezone.now())

                #Using the centrify script here to pull the Active Directory Zone
                if centrify_is_installed:
                    #Since we're using adinfo to find the zone, it fits that it should be here in the centrify script
                    stdin, stdout, stderr = client.exec_command('adinfo | grep Zone')
                    #print stdout.readlines()[0]
                    x = stdout.readlines()[0].split("/")
                    zone_tmp = x[4].rstrip()
                    zone = Zone.objects.get(name=zone_tmp)

                    LinuxServer.objects.filter(name=server, exception=False, active=True).update(zone=zone)
                    


#start execution
if __name__ == '__main__':
    print "Checking centrify version..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    from server.models import LinuxServer
    update_server()
    elapsed_time= timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
