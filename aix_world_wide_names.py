#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to get aix world wide names for the storage group
#
# Boomer Rehfield - 8/13/2015
#
#########################################################################

import os
import sys
import re
from paramiko import SSHClient

# these are need in django 1.7 and needed vs the django settings command
import django

from server.models import AIXServer, AIXWorldWideName
import logging
import utilities

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

    try:
        AIXWorldWideName.objects.all().delete()
    except:
        pass

    for frame in frames:

        print frame
        command = 'lshwres -r virtualio --rsubtype fc --level lpar -m ' + frame.rstrip() + ' |cut -d, -f1,10,11|cut -d= -f2,3|grep -v vio'
        # print command

        stdin, stdout, stderr = client.exec_command(command)

        data = stdout.readlines()

        for line in data:
            line = line.rstrip()
            # print line
            if line == "No results were found.":
                continue
            find = re.compile(r"^[^,]*")
            name = re.search(find, line).group(0)

            # print name
            wwn = re.findall(",(.*)$", line)
            wwn = wwn[0]
            wwn = re.sub(r'"wwpns=', '', wwn)
            wwn = re.sub(r'"', '', wwn)
            wwn = wwn.split(',')

            wwn1 = wwn[0]
            wwn2 = wwn[1]

            server = AIXServer.objects.get(name=name)

            # Need to go to the lpar and get the
            # GET THE WHAT?!?! WE NEED TO KNOW!!!
            if utilities.ping(server):

                client2 = SSHClient()

                if utilities.ssh(server, client2):

                    # get the list of fiber channel adapters
                    command2 = 'lscfg | grep fcs'
                    stdin, stdout, stderr = client2.exec_command(command2)

                    fc_list = []

                    for line2 in stdout.readlines():

                        line2 = line2.split(' ')[1]
                        fc_list.append(line2)

                    # figure out which adapter these belong to
                    correct_fc = ''
                    for fc in fc_list:
                        command2 = "lscfg -vpl " + fc + "|grep 'Network Address'|awk -F '.' '{print $14}'"
                        stdin, stdout, stderr = client2.exec_command(command2)
                        output = stdout.readlines()[0].rstrip().lower()
                        print 'fc = ' + fc
                        print 'output = ' + output
                        if output == wwn1:
                            correct_fc = fc
            print server
            print wwn1
            print wwn2
            print fc_list[0]
            print fc_list[1]
            print "Correct Fiber channel = " + correct_fc
            AIXWorldWideName.objects.get_or_create(name=server, fiber_channel_adapter=correct_fc, world_wide_name1=wwn1, world_wide_name2=wwn2)


if __name__ == '__main__':
    print "Starting population..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    populate()
