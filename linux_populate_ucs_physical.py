#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# UCS Linux Physical populate script
#
# Boomer Rehfield - 8/7/2014
#
#########################################################################

import os, sys
from ssh import SSHClient
#import paramiko
import utilities
from django.utils import timezone
from subprocess import call, check_output


from django.contrib.admin.models import LogEntry

#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import LinuxServer, Zone, Frame, Stack
#import logging
django.setup()

#logging.basicConfig( level=logging.INFO )

def populate():

    server_list = ('dinfdhp00',
                'dinfhdp01', 'dinfhdp02', 'dinfhdp03',
                'dinfhdp04', 'dinfhdp05', 'dinfhdp06',
                'dinfhdp07', 'dinfhdp08', 'dinfhdp09',
                'dinfipcbd01',
                'pinfhdp00',
                'pinfhdp01', 'pinfhdp02', 'pinfhdp03', 'pinfhdp04', 'pinfhdp05',
                'pinfhdp06', 'pinfhdp07', 'pinfhdp08', 'pinfhdp09', 'pinfhdp10',
                'pinfhdp11', 'pinfhdp12', 'pinfhdp13', 'pinfhdp14', 'pinfhdp15',
                'pinfhdp16', 'pinfhdp17', 'pinfhdp18', 'pinfhdp19', 'pinfhdp20',
                'pinfhdp20', 'pinfhdp21', 'pinfhdp22', 'pinfhdp23', 'pinfhdp24',
                'pinfhdp25', 'pinfhdp26', 'pinfhdp27', 'pinfhdp28', 'pinfhdp29',
                'pinfhdp30', 'pinfhdp31',
                'uinfhdp00',
                'uinfhdp01', 'uinfhdp02', 'uinfhdp03', 'uinfhdp04', 'uinfhdp05',
                'uinfhdp06', 'uinfhdp07', 'uinfhdp08', 'uinfhdp09', 'uinfhdp10',
                'uinfhdp11', 'uinfhdp12', 'uinfhdp13', 'uinfhdp14', 'uinfhdp15',
                'uinfhdp20', 'uinfhdp21', 'uinfhdp22', 'uinfhdp23', 'uinfhdp24',
                'uinfhdp25', 'uinfhdp26', 'uinfhdp27', 'uinfhdp28', 'uinfhdp29',
                'uinfhdp30', 'uinfhdp31',
                'uinfipcbd01',
                'uinfpegapp01', 'uinfpegaapp02')
    for server_name in server_list:
        print server_name

        ns_command = 'nslookup ' + server_name + ' | grep Address | grep -v "#" '
        try:
            ip_address = check_output(ns_command, shell=True)
            ip_address = ip_address[9:]
        except:
            ip_address = '0.0.0.0'
        
        #This is set when the centrify script runs, no sense in doing it here
        zone = Zone.objects.get(name='Unsure')


        try:
            server = LinuxServer.objects.get(name=server_name.rstrip())
        except:
            print server_name.rstrip()
            print len(server_name.rstrip())
            #the created object is not the same, so we create it and then get the instance
            #setting exception to True so the ssh keys script will pick it up and transfer keys
            server = LinuxServer.objects.get_or_create(name=str(server_name).rstrip(), owner='None', vmware_cluster='Physical', adapter='None', active=True, exception=False, decommissioned=False, created=timestamp, modified=timestamp, ip_address=ip_address, zone=zone, os='RHEL', os_level='None', memory=0, cpu=0, storage=0, centrify='None', xcelys='None', bash='None', ssl='None', java='None', impervaxl='None', netbackup='None', log='None')
            server = LinuxServer.objects.get(name=server_name.rstrip())
            change_message = "Added Linux Server " + server_name.rstrip() + "."
            LogEntry.objects.create(action_time=timezone.now(), user_id=11 ,content_type_id=9, object_id =264, object_repr=server, action_flag=1, change_message=change_message)
        




#start execution
if __name__ == '__main__':
    print "Starting populations..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    populate()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)




