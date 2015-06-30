#!/bin/bash

#script to activate virtualenv and run all of the other scripts in order

cd /home/wrehfiel/ENV/dashboard
#source bin/activate

export DJANGO_SETTINGS_MODULE=dashboard.settings


#mail william.rehfield@wellcare.com -s 'starting linux populate' < 1.txt
#/home/wrehfiel/ENV/dashboard/linux_populate.pl
mail william.rehfield@wellcare.com -s 'starting linux ssh keys' < 1.txt
/home/wrehfiel/ENV/dashboard/ssh_keys.py --linux all
mail william.rehfield@wellcare.com -s 'starting linux bash' < 1.txt
/home/wrehfiel/ENV/dashboard/linux_bash.py
mail william.rehfield@wellcare.com -s 'starting linux centrify' < 1.txt
/home/wrehfiel/ENV/dashboard/linux_centrify.py
mail william.rehfield@wellcare.com -s 'starting linux netbackup' < 1.txt
/home/wrehfiel/ENV/dashboard/linux_netbackup.py
mail william.rehfield@wellcare.com -s 'starting linux oslevel' < 1.txt
/home/wrehfiel/ENV/dashboard/linux_oslevel.py
mail william.rehfield@wellcare.com -s 'starting linux ssl' < 1.txt
/home/wrehfiel/ENV/dashboard/linux_ssl.py
#/home/wrehfiel/ENV/dashboard/linux_storage.py
mail william.rehfield@wellcare.com -s 'starting linux xcelys' < 1.txt
/home/wrehfiel/ENV/dashboard/linux_xcelys.py
mail william.rehfield@wellcare.com -s 'starting linux syslog' < 1.txt
/home/wrehfiel/ENV/dashboard/linux_syslog.py
mail william.rehfield@wellcare.com -s 'starting linux rsyslog_r' < 1.txt
/home/wrehfiel/ENV/dashboard/linux_rsyslog_r.py
#put something in here to shoot me an email
/home/wrehfiel/ENV/dashboard/historical_data_linux.py
mail william.rehfield@wellcare.com -s 'finished linux scripts' < 1.txt
