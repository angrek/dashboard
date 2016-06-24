#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to get processor pool data for each frame
#
# Boomer Rehfield - 6/22/2015
#
#########################################################################

import os
import sys
from ssh import SSHClient
from decimal import Decimal

# these are need in django 1.7 and needed vs the django settings command
import django
from django.utils import timezone

from server.models import AIXProcPool, Frame, Power7Inventory
import logging

django.setup()

logging.basicConfig(level=logging.INFO)


def populate():

    f = open("../../.ssh/p", "r")

    # need rstrip to strip off the newline at the end
    password = str(f.read().rstrip())
    f.close()
    client = SSHClient()
    client.load_system_host_keys()

    try:
        client.connect('phmc01', username="wrehfiel", password=password)
    except:
        print 'SSH to phmc01 has failed!'
        sys.exit()

    # Grab all of the frames on the HMC
    stdin, stdout, stderr = client.exec_command('lssyscfg -r sys -F name')

    frames = stdout.readlines()
    for frame in frames:
        # the output is throwing newlines at the end of the names for some reason
        # hence the use of rstrip below

        client = SSHClient()
        client.load_system_host_keys()

        # we've already established a connect6ion, but should put in error checking
        # FIXME
        client.connect('phmc01', username="wrehfiel", password=password)

        types = ['procpool']

        for type in types:
            # for each frame, let's get all of the HMC memory data
            command = 'lshwres -r ' + type + ' -m ' + frame.rstrip()
            # print command

            stdin, stdout, stderr = client.exec_command(command)
            pool_data = stdout.readlines()

            for line in pool_data:
                line = line.rstrip()
                if line != "The managed system does not support multiple shared processor pools.":
                    x = line.split(',')
                    if x[0] != "name=DefaultPool":
                        pool_name = x[0].rstrip()[5:]
                        max_proc_units = x[2].rstrip()[20:]
                        frame = frame.rstrip()
                        print "++++++++++++++++++++++++++++"
                        print "Frame: " + frame
                        print "---------------------------------------------------"
                        # full out put of the command,
                        # print line.rstrip()
                        # print "-----------------------------------"
                        # name
                        print ">>" + x[0]
                        # shared_prod_pool_id
                        # print x[1]
                        # max_pool_proc_units
                        print ">>>" + x[2]
                        # curr_reserved_pool_proc_units
                        # print x[3]
                        # pend_reserved_pool_proc_units
                        # print x[4]

                        # Need to get the used proc units from power 7 table
                        # used_proc_units = 200

                        frame_obj = Frame.objects.get(name=frame)
                        server_list = Power7Inventory.objects.filter(frame=frame_obj, curr_shared_proc_pool_name=pool_name)
                        used_proc_units = 0
                        curr_procs = 0
                        print "======================"
                        for server in server_list:
                            print "-" + str(server.name) + " - " + str(server.curr_shared_proc_pool_name) + " - " + str(server.curr_proc_units)
                            used_proc_units += Decimal(server.curr_proc_units)
                            curr_procs += Decimal(server.curr_procs)
                        print "MAX PROC UNITS:  " + str(max_proc_units)
                        print "USED PROC UNITS: " + str(used_proc_units)
                        print "CURR (VIRT) PROCS: " + str(curr_procs)

                        print "======================"

                        try:
                            pool_data = AIXProcPool.objects.get(frame=frame_obj, pool_name=pool_name)
                            pool_data.max_proc_units = max_proc_units
                            pool_data.used_proc_units = used_proc_units
                            pool_data.curr_procs = curr_procs
                            pool_data.modified = timezone.now()
                            pool_data.save()
                        except:
                            pool_data = AIXProcPool.objects.get_or_create(frame=frame_obj, pool_name=pool_name, max_proc_units=max_proc_units, used_proc_units=used_proc_units, curr_procs=curr_procs, modified=timezone.now())

                        # change_message = "Server is now inactive. Set active to False"
                        # LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)
#                except:
#                    AIXServer.objects.get_or_create(name=server.rstrip(), frame=frame.rstrip(), os='AIX', active=False)


if __name__ == '__main__':
    print "Checking AIX Proc Pools..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    populate()
