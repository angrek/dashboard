#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Yay, backup script!
#
# Boomer Rehfield - 2/4/2015
#
#########################################################################

import os

# these are need in django 1.7 and needed vs the django settings command
from django.utils import timezone
import django

django.setup()


def run_backups():

    now = timezone.now()
    timestamp = timezone.localtime(now).strftime('%m.%d.%Y.%H%M')
    hour = timezone.localtime(now).strftime('%H')
    month = timezone.localtime(now).strftime('%m')
    day = timezone.localtime(now).strftime('%d')
    # year = timezone.localtime(now).strftime('%Y')

    if hour == '01':
        command = 'rm -fr /home/wrehfiel/ENV/dashboard/mysql/*hourly*'
        os.system(command)
        filename = 'dashboard.daily.' + timestamp + '.mysql'
    else:
        filename = 'dashboard.hourly.' + timestamp + '.mysql'

    command = 'mysqldump dashboard > /home/wrehfiel/ENV/dashboard/mysql/' + filename
    os.system(command)

    command = 'gzip /home/wrehfiel/ENV/dashboard/mysql/*.mysql'
    os.system(command)
    # command =

    if day == '15':
        # FIXME need to fix the backups before Jan 2016 rolls around!
        month = int(month) - 1
        if len(str(month)) < 2:
            month = '0' + str(month)
        command = 'rm -fr /home/wrehfiel/ENV/dashboard/mysql/dashboard.daily.' + month + '*'
        os.system(command)

        # command = 'echo "Unix Configuration Report" | mutt -a "' + filename + '" -s "Unix Configuration Report" -- boomer@wellcare.com'
        # os.system(command)


if __name__ == '__main__':
    print "Running backups..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    run_backups()

    # print "Elapsed time: " + str(elapsed_time)
