#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Python script to create dynamic inventory files for Ansible based
# on queries to Lizardfish's ORM database connector.
#
# Boomer Rehfield - 1/22/2016
#
#########################################################################

import os
import argparse
import textwrap
import subprocess
import sys
import operator

# I'm pretty sure this needs to be here for others to use this file before the import
os.environ['DJANGO_SETTINGS_MODULE'] = 'dashboard.settings'
# these are need in django 1.7 and needed vs the django settings command
import django
from django.db.models import Q

from server.models import AIXServer, LinuxServer
django.setup()


# command line arguments and usage
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\

    This is a script to query Lizardfish's database to create Ansible inventory files.
    It will filter your query based on available fields in the database. See available below.

    You must at least use the --os argument to know what database table to query.
    You may only use the --os arg once.

    Examples:
    ./ansible.py --os linux                                             #Return all Linux servers (must be lowercase)
    ./ansible.py --os aix                                               #Return all AIX servers
    ./ansible.py --os linux --zone production                           #All Linux prod servers
    ./ansible.py --os aix --zone nonproduction                          #All AIX nonprod servers
    ./ansible.py --os aix --name__contains sas                          #This is a straight query for 'sas'.
    ./ansible.py --os linux --zone production --name__contains esb      #Give me prod ESB linux boxes


    You would want to redirect the output to your inventory file:
    ./ansible.py --os aix > aix_servers

    So with SSH form and ansible server, your command would look something like this:
    ssh p1rhrep /home/wrehfiel/ENV/dashboard/ansible.py --os linux --os_level 5.10 > testing

    '''))

parser.add_argument('--os', help="aix or linux (lowercase)")
parser.add_argument('--os_level', help="Check for a specific version of the OS")
parser.add_argument('--zone', help="production or nonproduction (lowercase)")
parser.add_argument('--name__contains', help="Can be full or partial matching name of a server.")
parser.add_argument('--centrify', help="Centrify version")
parser.add_argument('--centrifyda', help="Centrify Direct Audit version")
parser.add_argument('--xcelys', help="Xcelys version")
parser.add_argument('--bash', help="Bash version")
parser.add_argument('--ssl', help="SSL version")
parser.add_argument('--netbackup', help="Netbackup version")
parser.add_argument('--syslog', help="Syslog version")
parser.add_argument('--rsyslog', help="Rsyslog version")
parser.add_argument('--samba', help="Samba version")
parser.add_argument('--python', help="Python version")
args = parser.parse_args()

# must specify arguments
if not args.os:
    print "Error! You MUST define the --os parameter."
    parser.print_help()
    sys.exit()


def update_server():
    # print 'args.os = ' + str(args.os)
    # print 'args.zone = ' + str(args.zone)
    # print 'args.name__contains = ' + str(args.name__contains)
    server_list = []

    # By default we want to pull back only non decommed servers
    predicates = [('decommissioned', False)]
    predicates.append(('active', True))

    # Operating system args
    if args.os:
        if args.os == 'aix':
            predicates.append(('os', 'AIX'))
        if args.os == 'linux':
            predicates.append(('os', 'RHEL'))

    # Active directory args
    # predicates.append(('zone', args.zone))
    if args.zone:
        if args.zone == 'production':
            predicates.append(('zone__id', 2))
        if args.zone == 'nonproduction':
            predicates.append(('zone__id', 1))

    # Let's get crazy with the cheese wiz
    if args.name__contains:
        predicates.append(('name__contains', args.name__contains))

    if args.os_level:
        predicates.append(('os_level', args.os_level))

    if args.centrify:
        predicates.append(('centrify', args.centrify))

    if args.centrifyda:
        predicates.append(('centrifyda', args.centrifyda))

    if args.xcelys:
        predicates.append(('xcelys', args.xcelys))

    if args.bash:
        predicates.append(('bash', args.bash))

    if args.ssl:
        predicates.append(('ssl', args.ssl))

    if args.netbackup:
        predicates.append(('netbackup', args.netbackup))

    if args.syslog:
        predicates.append(('syslog', args.syslog))

    if args.rsyslog:
        predicates.append(('rsyslog', args.rsyslog))

    if args.samba:
        predicates.append(('samba', args.samba))

    if args.python:
        predicates.append(('python', args.python))

    # Here we use python's Q to get all the predicates together
    q_list = [Q(x) for x in predicates]

    if args.os == 'aix':
        server_list = AIXServer.objects.filter(reduce(operator.and_, q_list))
    if args.os == 'linux':
        server_list = LinuxServer.objects.filter(reduce(operator.and_, q_list))

    print "[alpha]"
    # print server_list
    for server in server_list:
        print server.name


if __name__ == '__main__':
    # start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
