#!/bin/bash

#script to activate virtualenv and run all of the other scripts in order

cd /home/wrehfiel/ENV/dashboard
#source bin/activate

export DJANGO_SETTINGS_MODULE=dashboard.settings
mail william.rehfield@wellcare.com -s 'starting aix scripts' < 1.txt
mail robert.blayet@wellcare.com -s 'starting aix scripts' < 1.txt

mail william.rehfield@wellcare.com -s 'starting aix populate' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_populate.py
mail william.rehfield@wellcare.com -s 'starting aix power7 inventory' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_power7_inventory.py
mail william.rehfield@wellcare.com -s 'starting aix powerha' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_powerha.py
mail william.rehfield@wellcare.com -s 'starting aix ssh keys' < 1.txt
/home/wrehfiel/ENV/dashboard/ssh_keys.py --aix all
mail william.rehfield@wellcare.com -s 'starting aix bash' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_bash.py
mail william.rehfield@wellcare.com -s 'starting aix centrify' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_centrify.py
mail william.rehfield@wellcare.com -s 'starting aix emc' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_emc.py
mail william.rehfield@wellcare.com -s 'starting aix errpt' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_errpt.py
mail william.rehfield@wellcare.com -s 'starting aix imperva' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_imperva.py
mail william.rehfield@wellcare.com -s 'starting aix netbackup' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_netbackup.py
mail william.rehfield@wellcare.com -s 'starting aix oslevel' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_oslevel.py
mail william.rehfield@wellcare.com -s 'starting aix ssh_cent' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_ssh_cent.py
mail william.rehfield@wellcare.com -s 'starting aix ssh_aix' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_ssh.py
mail william.rehfield@wellcare.com -s 'starting aix ssl' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_ssl.py
mail william.rehfield@wellcare.com -s 'starting aix storage' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_storage.py
mail william.rehfield@wellcare.com -s 'starting aix xcelys' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_xcelys.py
mail william.rehfield@wellcare.com -s 'starting aix rsyslog' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_rsyslog.py
/home/wrehfiel/ENV/dashboard/historical_data_aix.py
mail william.rehfield@wellcare.com -s 'aix scripts are done' < 1.txt
mail robert.blayet@wellcare.com -s 'aix scripts are done' < 1.txt

