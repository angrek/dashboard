#!/bin/bash

#script to activate virtualenv and run all of the other scripts in order

cd /home/wrehfiel/ENV/dashboard
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
/home/wrehfiel/ENV/dashboard/aix_netbackup.py
mail william.rehfield@wellcare.com -s aix_netbackup < 9.txt
/home/wrehfiel/ENV/dashboard/aix_ssh.py
mail william.rehfield@wellcare.com -s aix_ssh < 9.txt
/home/wrehfiel/ENV/dashboard/aix_ssh_cent.py
mail william.rehfield@wellcare.com -s aix_ssh_cent < 9.txt


/home/wrehfiel/ENV/dashboard/linux_bash.py
mail william.rehfield@wellcare.com -s linux_bash < 9.txt
/home/wrehfiel/ENV/dashboard/linux_centrify.py
mail william.rehfield@wellcare.com -s linux_centrify < 9.txt
/home/wrehfiel/ENV/dashboard/linux_imperva.py
mail william.rehfield@wellcare.com -s linux_imperva < 9.txt
/home/wrehfiel/ENV/dashboard/linux_netbackup.py
mail william.rehfield@wellcare.com -s linux_netbackup < 9.txt
/home/wrehfiel/ENV/dashboard/linux_oslevel.py
mail william.rehfield@wellcare.com -s linux_oslevel < 9.txt
/home/wrehfiel/ENV/dashboard/linux_ssl.py
mail william.rehfield@wellcare.com -s linux_ssl < 9.txt
#/home/wrehfiel/ENV/dashboard/linux_storage.py
mail william.rehfield@wellcare.com -s linux_storage < 9.txt
/home/wrehfiel/ENV/dashboard/linux_xcelys.py
mail william.rehfield@wellcare.com -s linux_xcelys < 9.txt
#put something in here to shoot me an email
mail william.rehfield@wellcare.com -s 'finished all scripts' < 9.txt
