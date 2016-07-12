#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to get centrify version
#
# Boomer Rehfield - 8/28/2014
#
#########################################################################

import os
from paramiko import SSHClient
from multiprocessing import Pool

# these are need in django 1.7 and needed vs the django settings command
from django.utils import timezone
import django

from server.models import AIXServer, Zone
import utilities

django.setup()


def update_server(server):

    new_centrify = ''

    if utilities.ping(server):

        client = SSHClient()
        if utilities.ssh(server, client):
            centrify = ''
            new_centrify = ''
            print server.name
            centrify_is_installed = 1

            stdin, stdout, stderr = client.exec_command('adinfo -v')

            try:
                centrify = stdout.readlines()[0]
                new_centrify = centrify[19:-2]
            except:
                new_centrify = "None"
                centrify_is_installed = 0
            # if it's the same version, we don't need to update the record
            if str(new_centrify) != str(server.centrify):
                utilities.log_change(server, 'Centrify', str(server.centrify), str(new_centrify))

                AIXServer.objects.filter(name=server, exception=False, active=True).update(centrify=new_centrify, modified=timezone.now())

            if centrify_is_installed:

                # Since we're using adinfo to find the zone, it fits that it should be here in the centrify script
                stdin, stdout, stderr = client.exec_command('adinfo | grep Zone')
                x = stdout.readlines()[0].split("/")
                zone_tmp = x[4].rstrip()
                zone = Zone.objects.get(name=zone_tmp)
                old_zone = str(server.zone)
                if str(old_zone) != str(zone):
                    utilities.log_change(server, 'Zone', str(old_zone), str(zone))
                    AIXServer.objects.filter(name=server, exception=False, active=True).update(zone=zone)

            stdin, stdout, stderr = client.exec_command('dainfo -v')
            centrifyda = ''
            new_centrifyda = ''
            try:
                centrifyda = stdout.readlines()[0]
                new_centrifyda = centrifyda[19:-2]
            except:
                new_centrifyda = "None"
            # if it's the same version, we don't need to update the record
            if str(new_centrifyda) != str(server.centrifyda):
                utilities.log_change(server, 'CentrifyDA', str(server.centrifyda), str(new_centrifyda))

                AIXServer.objects.filter(name=server, exception=False, active=True).update(centrifyda=new_centrifyda, modified=timezone.now())


if __name__ == '__main__':
    print "Checking centrify version..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = AIXServer.objects.filter(decommissioned=False).exclude(name__contains='vio')

    pool = Pool(10)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
