#!/bin/bash

#script to activate virtualenv and run all of the other scripts in order

cd /home/wrehfiel/ENV/dashboard
#source bin/activate

export DJANGO_SETTINGS_MODULE=dashboard.settings
/home/wrehfiel/ENV/dashboard/aix_bash.py
mail william.rehfield@wellcare.com -s aix_bash < 1.txt
/home/wrehfiel/ENV/dashboard/aix_centrify.py
mail william.rehfield@wellcare.com -s aix_centrify < 1.txt
/home/wrehfiel/ENV/dashboard/aix_errpt.py
mail william.rehfield@wellcare.com -s aix_errpt < 1.txt
/home/wrehfiel/ENV/dashboard/aix_imperva.py
mail william.rehfield@wellcare.com -s aix_imperva < 1.txt
/home/wrehfiel/ENV/dashboard/aix_oslevel.py
mail william.rehfield@wellcare.com -s aix_oslevel < 1.txt
/home/wrehfiel/ENV/dashboard/aix_ssl.py
mail william.rehfield@wellcare.com -s aix_ssl < 1.txt
/home/wrehfiel/ENV/dashboard/aix_storage.py
mail william.rehfield@wellcare.com -s aix_storage < 1.txt
/home/wrehfiel/ENV/dashboard/aix_xcelys.py
mail william.rehfield@wellcare.com -s aix_xcelys < 1.txt
/home/wrehfiel/ENV/dashboard/aix_netbackup.py
mail william.rehfield@wellcare.com -s aix_netbackup < 1.txt
/home/wrehfiel/ENV/dashboard/aix_ssh.py
mail william.rehfield@wellcare.com -s aix_ssh < 1.txt
/home/wrehfiel/ENV/dashboard/aix_ssh_cent.py
mail william.rehfield@wellcare.com -s aix_ssh_cent < 1.txt


/home/wrehfiel/ENV/dashboard/linux_bash.py
mail william.rehfield@wellcare.com -s linux_bash < 1.txt
/home/wrehfiel/ENV/dashboard/linux_centrify.py
mail william.rehfield@wellcare.com -s linux_centrify < 1.txt
/home/wrehfiel/ENV/dashboard/linux_imperva.py
mail william.rehfield@wellcare.com -s linux_imperva < 1.txt
/home/wrehfiel/ENV/dashboard/linux_netbackup.py
mail william.rehfield@wellcare.com -s linux_netbackup < 1.txt
/home/wrehfiel/ENV/dashboard/linux_oslevel.py
mail william.rehfield@wellcare.com -s linux_oslevel < 1.txt
/home/wrehfiel/ENV/dashboard/linux_ssl.py
mail william.rehfield@wellcare.com -s linux_ssl < 1.txt
#/home/wrehfiel/ENV/dashboard/linux_storage.py
mail william.rehfield@wellcare.com -s linux_storage < 1.txt
/home/wrehfiel/ENV/dashboard/linux_xcelys.py
mail william.rehfield@wellcare.com -s linux_xcelys < 1.txt
#put something in here to shoot me an email
mail william.rehfield@wellcare.com -s 'finished all scripts' < 1.txt
