#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to look for Oracle database instances running
#
# Boomer Rehfield - 4/18/2016
#
#########################################################################

import os, re
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer
import utilities
import paramiko
from multiprocessing import Pool
django.setup()

db_list = []
dupe_list = []

def update_server(server):

        
    if utilities.ping(server):

        client = paramiko.SSHClient()
        if utilities.ssh(server, client):
            command = 'ps -ef | grep -i pmon | grep -v grep | grep -v ASM'
            stdin, stdout, stderr = client.exec_command(command)
            lines = stdout.readlines()
            db_name = ''
            for line in lines:
                line = line.rstrip()
                line = line.split(' ')
                print server.name
                db_name = line[-1]
                print db_name
                if db_name in db_list:
                    print "DUPLICATE!"
                    #duplicates = duplicates + 1
                    dupe_list.append(db_name)
                    print "-----------Duplicates----------"
                    print dupe_list
                db_list.append(db_name)


if __name__ == '__main__':
    print "Looking for Oracle databases"
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = AIXServer.objects.filter(decommissioned=False, active=True)

    duplicates = 0
    pool = Pool(30)
    pool.map(update_server, server_list)

    print "Duplicates"
    print "------------------------------"
    print dupe_list
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

