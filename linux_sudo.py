#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve sudo versions and drop them into Django dashboard
#
# Boomer Rehfield - 12/24/2015
#
# ## THIS IS NOT IN THE DATABASE!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#########################################################################

import os
import paramiko
from multiprocessing import Pool

# these are need in django 1.7 and needed vs the django settings command
from django.utils import timezone
import django

from server.models import LinuxServer
import utilities
django.setup()


def update_server(server):

    if utilities.ping(server):

        client = paramiko.SSHClient()

        if utilities.ssh(server, client):
            command = 'dzdo sudo -V | grep version | grep -v Sudoers'
            stdin, stdout, stderr = client.exec_command(command)
            sudo_version = stdout.readlines()[0].rstrip()

            # bash_version = re.sub(r'x86_64', '', bash_version)
            # print sudo_version
            if '1.8' not in sudo_version:
                print server.name + ' - ' + sudo_version
                # print sudo_version
            # print timezone.now()
            # check existing value, if it exists, don't update
            # if str(bash_version) != str(server.bash):
            #    utilities.log_change(server, 'bash', str(server.bash), str(bash_version))
            #    LinuxServer.objects.filter(name=server, exception=False, active=True).update(bash=bash_version, modified=timezone.now())


if __name__ == '__main__':
    print "Checking Bash versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = LinuxServer.objects.filter(decommissioned=False)

    pool = Pool(20)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
