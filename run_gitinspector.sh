#!/bin/bash

#script to activate virtualenv and run all of the other scripts in order

cd /home/wrehfiel/ENV/dashboard
#source bin/activate

export DJANGO_SETTINGS_MODULE=dashboard.settings
mail william.rehfield@wellcare.com -s 'starting aix scripts' < 1.txt

/home/wrehfiel/ENV/bin/python /home/wrehfiel/ENV/dashboard/gitinspector/gitinspector/gitinspector.py --format=html -x author:Peter -x author:Lee --timeline --since=2013-01-01 -w /home/wrehfiel/ENV/dashboard > /home/wrehfiel/ENV/dashboard/server/templates/server/git_stats_dashboard.html

