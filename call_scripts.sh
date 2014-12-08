#!/bin/bash

#script to activate virtualenv and run all of the other scripts in order

cd /home/wrehfiel/ENV/dashboard
#source bin/activate

export DJANGO_SETTINGS_MODULE=dashboard.settings
/home/wrehfiel/ENV/dashboard/aix_bash.py
mail william.rehfield@wellcare.com -s 'starting aix scripts' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_centrify.py
/home/wrehfiel/ENV/dashboard/aix_errpt.py
/home/wrehfiel/ENV/dashboard/aix_imperva.py
/home/wrehfiel/ENV/dashboard/aix_oslevel.py
/home/wrehfiel/ENV/dashboard/aix_ssl.py
/home/wrehfiel/ENV/dashboard/aix_storage.py
/home/wrehfiel/ENV/dashboard/aix_xcelys.py
/home/wrehfiel/ENV/dashboard/aix_netbackup.py
/home/wrehfiel/ENV/dashboard/aix_ssh.py
/home/wrehfiel/ENV/dashboard/aix_ssh_cent.py
/home/wrehfiel/ENV/dashboard/aix_emc.py
mail william.rehfield@wellcare.com -s 'aix scripts are done' < 1.txt


mail william.rehfield@wellcare.com -s 'starting linux scripts' < 1.txt
/home/wrehfiel/ENV/dashboard/linux_bash.py
/home/wrehfiel/ENV/dashboard/linux_centrify.py
/home/wrehfiel/ENV/dashboard/linux_imperva.py
/home/wrehfiel/ENV/dashboard/linux_netbackup.py
/home/wrehfiel/ENV/dashboard/linux_oslevel.py
/home/wrehfiel/ENV/dashboard/linux_ssl.py
#/home/wrehfiel/ENV/dashboard/linux_storage.py
/home/wrehfiel/ENV/dashboard/linux_xcelys.py
#put something in here to shoot me an email
mail william.rehfield@wellcare.com -s 'finished all scripts' < 1.txt
