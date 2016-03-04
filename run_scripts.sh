#!/bin/bash

#script to activate virtualenv and run all of the other scripts in order

cd /home/wrehfiel/ENV/dashboard
#source bin/activate

export DJANGO_SETTINGS_MODULE=dashboard.settings
mail william.rehfield@wellcare.com -s 'starting aix scripts' < 1.txt

mail william.rehfield@wellcare.com -s 'starting aix populate' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_populate.py
mail william.rehfield@wellcare.com -s 'starting aix ssh keys' < 1.txt
/home/wrehfiel/ENV/dashboard/ssh_keys.py --aix all

mail william.rehfield@wellcare.com -s 'starting decom ping sweep' < 1.txt
/home/wrehfiel/ENV/dashboard/x_ping_sweep_decommed.py

mail william.rehfield@wellcare.com -s 'starting aix power7 inventory' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_power7_inventory.py

mail william.rehfield@wellcare.com -s 'starting aix historical proc pools' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_proc_pools.py

mail william.rehfield@wellcare.com -s 'starting aix historical proc pools' < 1.txt
/home/wrehfiel/ENV/dashboard/historical_proc_pools.py

mail william.rehfield@wellcare.com -s 'starting aix affinity' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_affinity.py

mail william.rehfield@wellcare.com -s 'starting aix frame firmware' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_frame_firmware.py
mail william.rehfield@wellcare.com -s 'starting aix asm' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_asm.py
mail william.rehfield@wellcare.com -s 'starting aix efix' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_efix.py
mail william.rehfield@wellcare.com -s 'starting aix tmef' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_tmef.py
mail william.rehfield@wellcare.com -s 'starting aix powerha' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_powerha.py
mail william.rehfield@wellcare.com -s 'starting aix bash' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_bash.py
mail william.rehfield@wellcare.com -s 'starting aix centrify' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_centrify.py
mail william.rehfield@wellcare.com -s 'starting aix emc' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_emc.py
#mail william.rehfield@wellcare.com -s 'starting aix errpt' < 1.txt
#/home/wrehfiel/ENV/dashboard/aix_errpt.py
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
#mail william.rehfield@wellcare.com -s 'starting aix storage' < 1.txt
#/home/wrehfiel/ENV/dashboard/aix_storage.py
mail william.rehfield@wellcare.com -s 'starting aix xcelys' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_xcelys.py
mail william.rehfield@wellcare.com -s 'starting aix rsyslog' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_rsyslog.py
mail william.rehfield@wellcare.com -s 'starting aix user local' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_user_local.py
mail william.rehfield@wellcare.com -s 'starting aix ping decoms' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_ping_decoms.py
mail william.rehfield@wellcare.com -s 'starting aix wwns' < 1.txt
/home/wrehfiel/ENV/dashboard/aix_world_wide_names.py

/home/wrehfiel/ENV/dashboard/historical_data_aix.py
mail william.rehfield@wellcare.com -s 'aix scripts are done' < 1.txt


mail william.rehfield@wellcare.com -s 'starting linux populate' < 1.txt
/home/wrehfiel/ENV/dashboard/linux_populate.pl
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
mail william.rehfield@wellcare.com -s 'starting linux samba' < 1.txt
/home/wrehfiel/ENV/dashboard/linux_samba.py
mail william.rehfield@wellcare.com -s 'starting linux syslog' < 1.txt
/home/wrehfiel/ENV/dashboard/linux_syslog.py
mail william.rehfield@wellcare.com -s 'starting linux rsyslog_r' < 1.txt
/home/wrehfiel/ENV/dashboard/linux_rsyslog_r.py
mail william.rehfield@wellcare.com -s 'starting linux python' < 1.txt
/home/wrehfiel/ENV/dashboard/linux_python.py
#put something in here to shoot me an email
/home/wrehfiel/ENV/dashboard/historical_data_linux.py
mail william.rehfield@wellcare.com -s 'finished all scripts' < 1.txt
