#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# UCS Linux Physical populate script
#
# Boomer Rehfield - 8/7/2014
#
#########################################################################

import os
from subprocess import check_output

# these are need in django 1.7 and needed vs the django settings command
import django
from django.contrib.admin.models import LogEntry
from django.utils import timezone

from server.models import LinuxServer, Zone
django.setup()


def populate():
                # UCSMGR5
                    # Hadoop DEV
    server_list = ('dinfdhp00',
                   'dinfhdp01', 'dinfhdp02', 'dinfhdp03', 'dinfhdp04', 'dinfhdp05',
                   'dinfhdp06', 'dinfhdp07', 'dinfhdp08', 'dinfhdp09', 'dinfhdp10',
                   'dinfhdp11',

                   # Hadoop UAT
                   'uinfhdp00',
                   'uinfhdp01', 'uinfhdp02', 'uinfhdp03', 'uinfhdp04', 'uinfhdp05',
                   'uinfhdp06', 'uinfhdp07', 'uinfhdp08', 'uinfhdp09', 'uinfhdp10',
                   'uinfhdp11', 'uinfhdp12', 'uinfhdp13', 'uinfhdp14', 'uinfhdp15',
                   'uinfhdp20', 'uinfhdp21', 'uinfhdp22', 'uinfhdp23', 'uinfhdp24',
                   'uinfhdp25', 'uinfhdp26', 'uinfhdp27', 'uinfhdp28', 'uinfhdp29',

                   # Hadoop PROD
                   'pinfhdp00',
                   'pinfhdp01', 'pinfhdp02', 'pinfhdp03', 'pinfhdp04', 'pinfhdp05',
                   'pinfhdp06', 'pinfhdp07', 'pinfhdp08', 'pinfhdp09', 'pinfhdp10',
                   'pinfhdp11', 'pinfhdp12', 'pinfhdp13', 'pinfhdp14', 'pinfhdp15',
                   'pinfhdp16', 'pinfhdp17', 'pinfhdp18', 'pinfhdp19', 'pinfhdp20',
                   'pinfhdp20', 'pinfhdp21', 'pinfhdp22', 'pinfhdp23', 'pinfhdp24',
                   'pinfhdp25', 'pinfhdp26', 'pinfhdp27', 'pinfhdp28', 'pinfhdp29',


                   # Data Warehouse
                   'dinfipcbd01',
                   'uinfipcbd01',
                   'pinfipcbd01',


                   # Greenplum DEV
                   'dgpmstr01', 'dgpmstr02',
                   'dgpseg01', 'dgpseg02', 'dgpseg03', 'dgpseg04', 'dgpseg05',
                   'dgpseg06', 'dgpseg07', 'dgpseg08', 'dgpseg09', 'dgpseg10',
                   'dgpseg11', 'dgpseg12', 'dgpseg13', 'dgpseg14', 'dgpseg15',
                   'dgpseg16',

                   # Greenplum PROD
                   'pgpmstr01', 'pgpmstr02',
                   'pgpseg01', 'pgpseg02', 'pgpseg03', 'pgpseg04', 'pgpseg05',
                   'pgpseg06', 'pgpseg07', 'pgpseg08', 'pgpseg09', 'pgpseg10',
                   'pgpseg11', 'pgpseg12', 'pgpseg13', 'pgpseg14', 'pgpseg15',
                   'pgpseg16',


                   # Informatica
                   'dinfatt01',
                   'dinfatt01',
                   'pinfatt01',

                   # Hadoop SAN box
                   'xudsprapst01',

                   # UCSMGR2
                   'p1webdb'

                   # ILOs
                   'pdlpap04', 'pdlpap05',

                   # InfoSec
                   'pidiiapst01',

                   # MarkLogic
                   'uimlogdbst01', 'uimlogdbst02',
                   'pimlogdbst01', 'pimlogdbst02', 'pimlogdbst03', 'pimlogdbst04')

    my_time = timezone.now()
    for server_name in server_list[:1]:
        server_name = server_name.rstrip()
        print server_name

        ns_command = 'nslookup ' + server_name + ' | grep Address | grep -v "#" '
        try:
            ip_address = check_output(ns_command, shell=True)
            ip_address = ip_address[9:]
        except:
            ip_address = '0.0.0.0'

        # if LinuxServer.objects.filter(name=server_name.rstrip()).exists():
        # update values
        #    pass
        # else:
        print server_name.rstrip()
        print len(server_name.rstrip())
        # the created object is not the same, so we create it and then get the instance
        # setting exception to True so the ssh keys script will pick it up and transfer keys
        if LinuxServer.objects.filter(name=server_name).exists():
            server = LinuxServer.objects.update(name=server_name, vmware_cluster='Physical', modified=my_time, ip_address=ip_address, os='RHEL')
        else:
            # This is set when the centrify script runs, no sense in doing it here
            zone = Zone.objects.get(name='Unsure')
            server = LinuxServer.objects.create(name=str(server_name).rstrip(), vmware_cluster='Physical', created=my_time, modified=my_time, ip_address=ip_address, zone=zone, os='RHEL', os_level='None')

        change_message = "Added or Updated Physical Linux Server " + server_name.rstrip() + "."
        LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=16, object_id=264, object_repr=server, action_flag=1, change_message=change_message)


if __name__ == '__main__':
    print "Starting physical populations..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    populate()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
