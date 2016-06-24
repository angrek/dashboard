#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script check if iptables is set to on in checkconfig
#
# Boomer Rehfield - 6/16/2016
#
#########################################################################

import os
import re
from ssh import SSHClient
from multiprocessing import Pool

# these are need in django 1.7 and needed vs the django settings command
import django
from django.utils import timezone

from server.models import LinuxServer
import utilities
django.setup()


def update_server(server):

    if utilities.ping(server):

        client = SSHClient()
        if utilities.ssh(server, client):
            command = 'dzdo chkconfig --list iptables'
            stdin, stdout, stderr = client.exec_command(command)
            worked = 0
            try:
                output = stdout.readlines()[0]
                worked = 1
            except:
                pass

            if worked:
                print output
                if re.search("3:on", output):
                    LinuxServer.objects.filter(name=server).update(iptables_on=1)
                    print '------------------------------------'
                    print server.name
                    print "Chkconfig ON"
                else:
                    LinuxServer.objects.filter(name=server).update(iptables_on=0)
                    print '------------------------------------'
                    print server.name
                    print "Chkconfig OFF"


if __name__ == '__main__':
    print "Checking iptables..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = LinuxServer.objects.filter(decommissioned=False)

    pool = Pool(20)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
