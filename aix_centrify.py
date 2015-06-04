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
from server.models import AIXServer, Zone
import utilities
django.setup()



def update_server():
    server_list = AIXServer.objects.filter(decommissioned=False)
    #server_list = AIXServer.objects.filter(zone=1, decommissioned=False).exclude(centrify='5.2.2-192')

    for server in server_list:

        new_centrify = ''

        #these are hardcoded because
        #none of the vio servers have Centrify installed on them
        server_exceptions = AIXServer.objects.filter(name__contains='vio')

        #Make sure the server is set to active and not an exception
        if str(server) not in server_exceptions:

            if utilities.ping(server):
                
                client = SSHClient()
                if utilities.ssh(server, client):
                    print server.name
                    centrify_is_installed = 1

                    stdin, stdout, stderr = client.exec_command('adinfo -v')

                    try:
                        centrify = stdout.readlines()[0]
                        new_centrify = centrify[19:-2]
                    except:
                        new_centrify = "None"
                        centrify_is_installed = 0
                    #if it's the same version, we don't need to update the record
                    if str(new_centrify) != str(server.centrify):
                        utilities.log_change(str(server), 'Centrify', str(server.centrify), str(new_centrify))

                        AIXServer.objects.filter(name=server, exception=False, active=True).update(centrify=new_centrify, modified=timezone.now())
                    if centrify_is_installed:

                        #Since we're using adinfo to find the zone, it fits that it should be here in the centrify script
                        stdin, stdout, stderr = client.exec_command('adinfo | grep Zone')
                        x = stdout.readlines()[0].split("/")
                        zone_tmp = x[4].rstrip()
                        zone = Zone.objects.get(name=zone_tmp)
                        old_zone = str(server.zone)
                        if str(old_zone) != str(zone):
                            utilities.log_change(str(server), 'Zone', str(old_zone), str(zone))
                            AIXServer.objects.filter(name=server, exception=False, active=True).update(zone=zone)
                            
                        


#start execution
if __name__ == '__main__':
    print "Checking centrify version..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    from server.models import AIXServer
    update_server()
    elapsed_time= timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
