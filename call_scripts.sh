#!/bin/bash

#script to activate virtualenv and run all of the other scripts in order

cd /home/wrehfiel/ENV/dashboard
#source bin/activate

export DJANGO_SETTINGS_MODULE=dashboard.settings
mail william.rehfield@wellcare.com -s 'starting aix scripts' < 1.txt
mail william.rehfield@wellcare.com -s 'starting aix bash' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_bash.py
mail william.rehfield@wellcare.com -s 'starting aix populate' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_populate.py
mail william.rehfield@wellcare.com -s 'starting aix bash' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_bash.py
mail william.rehfield@wellcare.com -s 'starting aix centrify' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_centrify.py
mail william.rehfield@wellcare.com -s 'starting aix errpt' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_errpt.py
mail william.rehfield@wellcare.com -s 'starting aix imperva' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_imperva.py
mail william.rehfield@wellcare.com -s 'starting aix oslevel' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_oslevel.py
mail william.rehfield@wellcare.com -s 'starting aix ssl' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_ssl.py
mail william.rehfield@wellcare.com -s 'starting aix storage' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_storage.py
mail william.rehfield@wellcare.com -s 'starting aix xcelys' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_xcelys.py
mail william.rehfield@wellcare.com -s 'starting aix netbackup' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_netbackup.py
mail william.rehfield@wellcare.com -s 'starting aix ssh_aix' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_ssh.py
mail william.rehfield@wellcare.com -s 'starting aix ssh_cent' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_ssh_cent.py
mail william.rehfield@wellcare.com -s 'starting aix emc' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_emc.py
mail william.rehfield@wellcare.com -s 'aix scripts are done' < 1.txt


mail william.rehfield@wellcare.com -s 'starting linux bash' < 1.txt
/home/wrehfiel/ENV/dashboard/linux_bash.py
mail william.rehfield@wellcare.com -s 'starting linux centrify' < 1.txt
/home/wrehfiel/ENV/dashboard/linux_centrify.py
mail william.rehfield@wellcare.com -s 'starting linux imperva' < 1.txt
/home/wrehfiel/ENV/dashboard/linux_imperva.py
mail william.rehfield@wellcare.com -s 'starting linux netbackup' < 1.txt
/home/wrehfiel/ENV/dashboard/linux_netbackup.py
mail william.rehfield@wellcare.com -s 'starting linux oslevel' < 1.txt
/home/wrehfiel/ENV/dashboard/linux_oslevel.py
mail william.rehfield@wellcare.com -s 'starting linux ssl' < 1.txt
/home/wrehfiel/ENV/dashboard/linux_ssl.py
#/home/wrehfiel/ENV/dashboard/linux_storage.py
mail william.rehfield@wellcare.com -s 'starting linux xcelys' < 1.txt
/home/wrehfiel/ENV/dashboard/linux_xcelys.py
#put something in here to shoot me an email
mail william.rehfield@wellcare.com -s 'finished all scripts' < 1.txt
