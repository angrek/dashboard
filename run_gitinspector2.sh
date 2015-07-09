#!/bin/bash

#script to activate virtualenv and run all of the other scripts in order

#cd /home/wrehfiel/ENV/dashboard
#source bin/activate

export DJANGO_SETTINGS_MODULE=dashboard.settings


/home/wrehfiel/ENV/dashboard/gitinspector/gitinspector/gitinspector.py --format=html --file=yaml,j2,cfg --timeline --since=2013-01-01 -w ssh://dacmapp01/home/wrehfiel/ansible-dev/ > /home/wrehfiel/ENV/dashboard/server/templates/server/git_stats_ansible_dev.html

