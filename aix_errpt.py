#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to get AIX errpts
#
# Boomer Rehfield - 9/8/2014
#
#########################################################################

import os
from paramiko import SSHClient
from multiprocessing import Pool

# these are need in django 1.7 and needed vs the django settings command
from django.utils import timezone
# from django.contrib.admin.models import LogEntry
import django

from server.models import AIXServer, Errpt
import utilities
django.setup()


def update_server(server):

    if utilities.ping(server):

        client = SSHClient()
        if utilities.ssh(server, client):
            stdin, stdout, stderr = client.exec_command('errpt | tail -n 20"')
            report = ''

            # we have to do errpt differently due to the way it is handled by stdout
            for line in stdout:
                report = report + str(line)
            if report == '':
                report = "The errpt was empty."

            # we don't care about the old record and we'll just add another
            Errpt.objects.get_or_create(name=server, report=report, modified=timezone.now())
            # FIXME do we want to log errpts?? It's only for the VIO servers....
            # LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)


if __name__ == '__main__':
    print "Getting Errpts..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = AIXServer.objects.filter(name__contains='vio')

    pool = Pool(20)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
