#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve EMC versions on the servers and drop them into Django dashboard
#
# Boomer Rehfield - 8/7/2014
#
#########################################################################

import os
import re
from ssh import SSHClient
import paramiko
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
import test_server
import dashboard_logging
django.setup()


def update_server():

#    server_list = AIXServer.objects.all()
    server_list = AIXServer.objects.filter(decommissioned=False)
    #server_list = AIXServer.objects.filter(name__contains='ufts')
    for server in server_list:

        if test_server.ping(server):

            client = SSHClient()
            if test_server.ssh(server, client):

                #get the emc_clariion version
                stdin, stdout, stderr = client.exec_command('lslpp -l | grep -i EMC.CLARIION.fcp | uniq')
                rows = stdout.readlines()

                if rows:
                    row = rows[0]
                    #split the lines and grab the first one
                    temp = row.split("\r")[0]
                    p = re.compile(r' +')
                    temp2 = p.split(temp)
                    emc_clar = temp2[2]

                    #if existing value is the same, don't update
                    if str(emc_clar) != str(server.emc_clar):
                        dashboard_logging.log_change(str(server), 'EMC_CLAR', str(server.emc_clar), str(emc_clar))
                        AIXServer.objects.filter(name=server).update(emc_clar=emc_clar, modified=timezone.now())


                #get the emc_sym disks
                stdin2, stdout2, stderr2 = client.exec_command('lslpp -l | grep -i EMC.Symmetrix.fcp | uniq')
                rows2 = stdout2.readlines()
                if rows2:
                    row = rows2[1]
                    temp = row.split("\r")[0]
                    p = re.compile(r' +')
                    temp2 = p.split(temp)
                    emc_sym = temp2[1]
                    #print server
                    #print 'emc_sym'
                    #print str(emc_sym)                    
                    #if existing value is the same, don't update
                    if str(emc_sym) != str(server.emc_sym):

                        dashboard_logging.log_change(str(server), 'EMC_SYM', str(server.emc_sym), str(emc_sym))

                        AIXServer.objects.filter(name=server).update(emc_sym=emc_sym, modified=timezone.now())



#start execution


#start execution
if __name__ == '__main__':
    print "Checking EMC versions..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    from server.models import AIXServer
    update_server()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
