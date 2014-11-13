#!/bin/bash

#script to activate virtualenv and run all of the other scripts in order

cd /home/wrehfiel/ENV/
#source bin/activate

export DJANGO_SETTINGS_MODULE=dashboard.settings
/home/wrehfiel/ENV/bin/python dashboard/aix_bash.py
mail william.rehfield@wellcare.com < 1.txt
/home/wrehfiel/ENV/bin/python dashboard/aix_centrify.py
mail william.rehfield@wellcare.com < 2.txt
python dashboard/aix_errpt.py
mail william.rehfield@wellcare.com < 3.txt
python dashboard/aix_imperva.py
mail william.rehfield@wellcare.com < 4.txt
python dashboard/aix_oslevel.py
mail william.rehfield@wellcare.com < 5.txt
python dashboard/aix_ssl.py
mail william.rehfield@wellcare.com < 6.txt
python dashboard/aix_storage.py
mail william.rehfield@wellcare.com < 7.txt
python dashboard/aix_xcelys.py
mail william.rehfield@wellcare.com < 8.txt


#put something in here to shoot me an email
