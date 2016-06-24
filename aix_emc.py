#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve EMC versions on the servers
#
# Boomer Rehfield - 12/8/2014
#
#########################################################################

import os
import re
from ssh import SSHClient
from multiprocessing import Pool

# these are need in django 1.7 and needed vs the django settings command
from django.utils import timezone
import django
import utilities

from server.models import AIXServer
django.setup()


def update_server(server):

    print server.name
    if utilities.ping(server):

        client = SSHClient()
        if utilities.ssh(server, client):

            # get the emc_clariion version
            stdin, stdout, stderr = client.exec_command('lslpp -l | grep -i EMC.CLARIION.fcp | uniq')
            rows = stdout.readlines()

            if rows:
                try:
                    row = rows[0]
                    # split the lines and grab the first one
                    temp = row.split("\r")[0]
                    p = re.compile(r' +')
                    temp2 = p.split(temp)
                    emc_clar = temp2[2]

                    # if existing value is the same, don't update
                    if str(emc_clar) != str(server.emc_clar):
                        utilities.log_change(server, 'EMC_CLAR', str(server.emc_clar), str(emc_clar))
                        AIXServer.objects.filter(name=server).update(emc_clar=emc_clar, modified=timezone.now())
                except:
                    pass

            # get the emc_sym disks
            stdin2, stdout2, stderr2 = client.exec_command('lslpp -l | grep -i EMC.Symmetrix.fcp | uniq')
            rows2 = stdout2.readlines()
            if rows2:
                try:
                    row = rows2[1]
                    temp = row.split("\r")[0]
                    p = re.compile(r' +')
                    temp2 = p.split(temp)
                    emc_sym = temp2[1]

                    if str(emc_sym) != str(server.emc_sym):

                        utilities.log_change(server, 'EMC_SYM', str(server.emc_sym), str(emc_sym))

                        AIXServer.objects.filter(name=server).update(emc_sym=emc_sym, modified=timezone.now())
                except:
                    pass


if __name__ == '__main__':
    print "Checking EMC versions..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = AIXServer.objects.filter(decommissioned=False)

    pool = Pool(20)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
