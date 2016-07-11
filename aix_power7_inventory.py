#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Django, AIX Power7 inventory scripts. This is for gathering the mem
#   and cpu stats right now from the HMC and drop it into Django.
#
# Ok, for now this may be called from main script (future plans)
# but the idea is that the server and frame checks will have already
# been done so if it's pulling it from the frame, then it should already
# be in the database. I 'think' get_or_create should work here fine..
# Testing for now....
#
# Boomer Rehfield - 9/22/2014
#
#########################################################################

import os
import sys
from paramiko import SSHClient

# these are need in django 1.7 and needed vs the django settings command
import django

from server.models import AIXServer, Power7Inventory
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
        # print frame.rstrip()

        client = SSHClient()
        client.load_system_host_keys()

        # we've already established a connect6ion, but should put in error checking
        # FIXME
        client.connect('phmc01', username="wrehfiel", password=password)

        types = ['proc', 'mem']

        for type in types:

            # for each frame, let's get all of the HMC memory data
            command = 'lshwres -r ' + type + ' -m ' + frame.rstrip() + ' --level lpar'
            print command

            stdin, stdout, stderr = client.exec_command(command)
            lpar_list = stdout.readlines()
            # we'll close the connection after the next section

            lpar_array = {}

            for lpar in lpar_list:

                lpar_dict = lpar.split(",")

                for entry in lpar_dict:
                    # test for an empty value
                    if entry:
                        a, b = entry.split('=')
                        lpar_array[a] = b

                # ok, first we want to get the lpar name and then remove it from the dict
                # NOTE: in the database it is FK to 'name'. When I created the server db
                # I just called it name so that's why there is a difference. I can't go back
                # and change it because it is populated with WPARs also.
                server_name = lpar_array['lpar_name']
                print server_name
                # deleting so we can iterate over all of the values
                del lpar_array['lpar_name']

                # in case the server is new since the last time it ran, we'll just create a blank server record and then update it.

                # Need this here because a reuse server is missing from somewhere but I don't know why
                try:
                    name = AIXServer.objects.get(name=server_name)
                except:
                    continue
                print name

                if name.decommissioned is False:

                    try:
                        Power7Inventory.objects.filter(name=name).update(frame=name.frame, active=name.active, exception=name.exception, decommissioned=name.decommissioned, stack=name.stack)
                    except Power7Inventory.DoesNotExist:
                        print 'Not found, creating'
                        Power7Inventory.objects.get_or_create(name=name, frame=name.frame, active=name.active, exception=name.exception, decommissioned=name.decommissioned, stack=name.stack)

                    for key, value in lpar_array.iteritems():
                        if value == 'null':
                            value = 0
                        print key, "=>", value
                        print "attempting to update value...."
                        Power7Inventory.objects.filter(name=name).update(**{key: value})
                else:
                    pass


if __name__ == '__main__':
    print "Starting populations..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    populate()
