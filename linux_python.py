#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve Python versions 
#
# Boomer Rehfield - 7/8/2015 
# test
#########################################################################

import os, re
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import LinuxServer
from multiprocessing import Pool
import utilities

django.setup()


def update_server(server):


    if utilities.ping(server):
        
        client = SSHClient()
        if utilities.ssh(server, client):
            print server.name 
            command = 'python -V'
            stdin, stdout, stderr = client.exec_command(command)

            #FIXME why the hell is the version info coming through in stderr?
            try:
                version = stderr.readlines()[0].rstrip()
                version = re.sub('Python ', '', version)
            except:
                version = 'None'
            print version

            #check existing value, if it exists, don't update
            if str(version) != str(server.python):
                utilities.log_change(server, 'python', str(server.python), str(version))

                LinuxServer.objects.filter(name=server).update(python=version, modified=timezone.now())
            client.close()



#start execution
if __name__ == '__main__':
    print "Checking Python versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = LinuxServer.objects.filter(decommissioned=False)

    pool = Pool(20)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

