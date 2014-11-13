#!/bin/bash

#script to activate virtualenv and run all of the other scripts in order

cd /home/wrehfiel/ENV/
#source bin/activate

export DJANGO_SETTINGS_MODULE=dashboard.settings
/home/wrehfiel/ENV/dashboard/aix_bash.py
mail william.rehfield@wellcare.com -s aix_bash < 1.txt
/home/wrehfiel/ENV/dashboard/aix_centrify.py
mail william.rehfield@wellcare.com -s aix_centrify < 2.txt
/home/wrehfiel/ENV/dashboard/aix_errpt.py
mail william.rehfield@wellcare.com -s aix_errpt < 3.txt
/home/wrehfiel/ENV/dashboard/aix_imperva.py
mail william.rehfield@wellcare.com -s aix_imperva < 4.txt
/home/wrehfiel/ENV/dashboard/aix_oslevel.py
mail william.rehfield@wellcare.com -s aix_oslevel < 5.txt
/home/wrehfiel/ENV/dashboard/aix_ssl.py
mail william.rehfield@wellcare.com -s aix_ssl < 6.txt
/home/wrehfiel/ENV/dashboard/aix_storage.py
mail william.rehfield@wellcare.com -s aix_storage < 7.txt
/home/wrehfiel/ENV/dashboard/aix_xcelys.py
mail william.rehfield@wellcare.com -s aix_xcelys < 8.txt


#put something in here to shoot me an email
