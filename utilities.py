#!/home/wrehfiel/ENV/bin/python2.7
####################################################
#
# utilities.py
#
# Script to ping the servers to see if they are up.
# If they are not, then set them as inactive in the
# Django Dashboard. -Boomer Rehfield 9/4/2014
#
####################################################

import os
from ssh import SSHClient
from django.utils import timezone
from django.contrib.admin.models import LogEntry
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer
import smtplib
from email.mime.text import MIMEText
import email.utils
import paramiko

django.setup()

#test ping...  I know, not a very descriptive name...
def ping(server):
    response = os.system("ping -c 1 " + str(server) + "> /dev/null 2>&1")
    if response == 0:

        if server.active == False:
            server.active=True
            server.modified=timezone.now()
            server.save()
            LogEntry.objects.create(action_time=timezone.now(), user_id=11 ,content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='Ping succeeded, changed to active.')
    else:

        if server.active == True:
            server.active=False
            server.modified=timezone.now()
            server.save()
            LogEntry.objects.create(action_time=timezone.now(), user_id=11 ,content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='Ping failed, changed to inactive.')

    #for the sake of brevetiy elsewhere, I'm flipping this. Returning 0 for a good result is stupid. *cough* Looking at you ping...
    if response == 0:
        response = 1
    else:
        response = 0
    return response


#test ssh... duh
def ssh(server, client):
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(str(server), username="wrehfiel", timeout=10)
        if server.exception == True:
            server.exception = False
            server.save()
            LogEntry.objects.create(action_time=timezone.now(), user_id=11 ,content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='SSH succeeded, changed exception.')
        response = 1

    except:
        if server.exception == False:
            server.exception = True
            server.save()
            LogEntry.objects.create(action_time=timezone.now(), user_id=11 ,content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='SSH failed, changed exception.')
        response = 0
    return response


def send_email(subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = email.utils.formataddr(('Boomer', "boomer\@wellcare.com"))
    msg['To'] = email.utils.formataddr(('Boomer', "boomer\@wellcare.com"))
    server = smtplib.SMTP('mail')
    server.sendmail("boomer@wellcare.com", "boomer@wellcare.com",msg.as_string())


def log_change(server, app, old_version, new_version):
    change_message = 'Changed ' + app + ' from ' + old_version + ' to ' + new_version
    LogEntry.objects.create(action_time='2014-08-25 20:00:00', user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)




