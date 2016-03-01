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
from server.models import Zone
from server.models import LinuxServer
import utilities
from multiprocessing import Pool
django.setup()



def update_server(server):

    centrify = ''
    new_centrify = ''
    if utilities.ping(server):
        client = SSHClient()
        if utilities.ssh(server, client):
            centrify_is_installed = 1
            stdin, stdout, stderr = client.exec_command('adinfo -v')
            print server
            try:
                centrify = stdout.readlines()[0]
                new_centrify = centrify[19:-2]
            except:
                new_centrify = "None"
                centrify_is_installed = 0

            #if it's the same version, we don't need to update the record
            if str(new_centrify) != str(server.centrify):
                utilities.log_change(server, 'Centrify', str(server.centrify), str(new_centrify))
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


            #Get CentrifyDA version
            centrifyda = ''
            new_centrifyda = ''
            stdin, stdout, stderr = client.exec_command('dainfo -v')
            print '1'
            try:
                centrifyda = stdout.readlines()[0]
                new_centrifyda = centrifyda[19:-2]
            except:
                new_centrifyda = "None"
                centrify_is_installed = 0

            #if it's the same version, we don't need to update the record
            if str(new_centrifyda) != str(server.centrifyda):
                utilities.log_change(server, 'CentrifyDA', str(server.centrifyda), str(new_centrifyda))
                LinuxServer.objects.filter(name=server, exception=False, active=True).update(centrifyda=new_centrifyda, modified=timezone.now())




#start execution
if __name__ == '__main__':
    print "Checking centrify version..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = LinuxServer.objects.filter(decommissioned=False)
    #server_list = LinuxServer.objects.filter(decommissioned=False).exclude(centrify='5.2.2-192')

    pool = Pool(20)
    pool.map(update_server, server_list)

    elapsed_time= timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
