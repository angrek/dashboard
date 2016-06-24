#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to gather lpar affinity data from the HMC
#
# Boomer Rehfield - 4/24/2015
#
#########################################################################

import os
import sys
from ssh import SSHClient

# these are need in django 1.7 and needed vs the django settings command
import django

from server.models import AIXServer
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
    for frame in frames:

        command = "lsmemopt -m " + frame.rstrip() + " -r lpar -o calcscore"
        print command

        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.readlines()

        # some of the frames don't support affinity
        for line in output:
            line = line.rstrip()
            if line[:8] == 'HSCLA012':
                continue
            print line
            line = line.split(',')
            name = line[0].split('=')[1]
            curr_lpar_score = line[2].split('=')[1]
            predicted_lpar_score = line[3].split('=')[1]
            print len(curr_lpar_score)
            if curr_lpar_score == 'none' or predicted_lpar_score == 'none':
                continue
            else:
                curr_lpar_score = int(curr_lpar_score)
                predicted_lpar_score = int(predicted_lpar_score)

            print name
            print curr_lpar_score
            print predicted_lpar_score

            server = AIXServer.objects.get(name=name)
            if server.curr_lpar_score_new != curr_lpar_score:
                print server.curr_lpar_score_new
                print curr_lpar_score
                # print len(server.curr_lpar_score)
                # print len(curr_lpar_score)
                utilities.log_change(server, 'AIX curr_lpar_score_new', str(server.curr_lpar_score_new), str(curr_lpar_score))
                server.curr_lpar_score_new = curr_lpar_score
                server.save()
            if server.predicted_lpar_score_new != predicted_lpar_score:
                utilities.log_change(server, 'AIX predicted_lpar_score_new', str(server.predicted_lpar_score_new), str(predicted_lpar_score))
                server.predicted_lpar_score_new = predicted_lpar_score
                server.save()
        print '-----------'


if __name__ == '__main__':
    print "Starting aix affinity..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    populate()
