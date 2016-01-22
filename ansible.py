#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve SSL versions on the servers and drop them into Django dashboard
#
# Boomer Rehfield - 8/7/2014
#
#########################################################################

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'dashboard.settings'
import re
from ssh import SSHClient
from django.utils import timezone
from server.models import AIXServer, LinuxServer

#need itertools to concatenate the query sets to combine lists of servers from two different tables
from itertools import chain

#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
import utilities
django.setup()
import paramiko
import getpass
import argparse
import textwrap
from subprocess import *
import sys

from django.db.models import Q
import operator

#command line arguments and usage
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\

    Set your SSH keys across active AIX and UNIX servers.

    You must use either the --aix or --linux arguments, or both.

    Example:
    ./ansible.py --os linux                 #return all linux servers (must be lowercase)
    ./ansible.py --os aix
    ./ansible.py --zone production                  #All production servers
    ./ansible.py --os aix --zone nonproduction       #All nonproduction aix servers
    ./ansible.py --name__contains p1sasgrid

    #NOTE: I am intentionally not including anything decommed. Why would
    we run ansible against a list of decoms??
    '''))

parser.add_argument('--os', help="aix or linux (lowercase)")
parser.add_argument('--zone', help="production or nonproduction (lowercase)")
parser.add_argument('--name__contains', help="Can be full or partial matching name of a server.")
parser.add_argument('--os_level', help="Check for a specific version of the OS")
args = parser.parse_args()

#must specify arguments
if not args.os:
    print "Error! You MUST define the --os parameter"
    parser.print_help()
    sys.exit()



def update_server():
    #print 'args.os = ' + str(args.os)
    #print 'args.zone = ' + str(args.zone)
    #print 'args.name__contains = ' + str(args.name__contains)
    server_list = []

    #By default we want to pull back only non decommed servers
    predicates = [('decommissioned', False)]

    #Operating system args
    if args.os:
        if args.os == 'aix':
            predicates.append(('os', 'AIX'))
        if args.os == 'linux':
            predicates.append(('os', 'RHEL')) 

    #Active directory args
    #predicates.append(('zone', args.zone))
    if args.zone:
        if args.zone == 'production':
            predicates.append(('zone__id', 2))
        if args.zone == 'nonproduction':
            predicates.append(('zone__id', 1))

    #Let's get crazy with the cheese wiz
    if args.name__contains:
        predicates.append(('name__contains', args.name__contains))

    if args.os_level:
        predicates.append(('os_level', args.os_level))

    q_list = [Q(x) for x in predicates]

    if args.os == 'aix':
        server_list = AIXServer.objects.filter(reduce(operator.and_, q_list))
    if args.os == 'linux':
        server_list = LinuxServer.objects.filter(reduce(operator.and_, q_list))

    print "[alpha]" 
    #print server_list
    for server in server_list:
        print server.name
    
    #print "Predicates a comnin'!"
    #print predicates


#start execution
if __name__ == '__main__':
    #print "Beginning test..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    #elapsed_time = timezone.now() - start_time
    #print "Elapsed time: " + str(elapsed_time)
