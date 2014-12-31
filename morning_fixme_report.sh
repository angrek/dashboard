#!/bin/bash

#script to activate virtualenv and run all of the other scripts in order

cd /home/wrehfiel/ENV/dashboard
#source bin/activate

export DJANGO_SETTINGS_MODULE=dashboard.settings


grep FIXME *.py > temp.txt
mail william.rehfield@wellcare.com -s 'Morning FIXME report' < temp.txt
rm temp.txt
