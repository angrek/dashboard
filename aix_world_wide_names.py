#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to get processor pool data for each frame
#
# Boomer Rehfield - 6/4/2015
#
#########################################################################

import os, sys, re
from ssh import SSHClient
from django.utils import timezone
from django.contrib.admin.models import LogEntry

#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer, Frame, AIXWorldWideName
import logging
from decimal import Decimal
django.setup()

logging.basicConfig( level=logging.INFO )

def populate():

    f = open("../../.ssh/p", "r")

    #need rstrip to strip off the newline at the end
    password = str(f.read().rstrip())
    f.close()
    client = SSHClient()
    client.load_system_host_keys()
    
    try:
        client.connect('phmc01', username="wrehfiel", password=password)
    except:
        print 'SSH to phmc01 has failed!'
        sys.exit()

    #Grab all of the frames on the HMC
    stdin, stdout, stderr = client.exec_command('lssyscfg -r sys -F name')

    frames = stdout.readlines()


    try:
        AIXWorldWideName.objects.all().delete()
    except:
        pass


    for frame in frames:
        print frame
        command = 'lshwres -r virtualio --rsubtype fc --level lpar -m ' + frame.rstrip() + ' |cut -d, -f1,10,11|cut -d= -f2,3|grep -v vio'
        #print command

        stdin, stdout, stderr = client.exec_command(command)

        data = stdout.readlines()
        for line in data:
            line = line.rstrip()
            print line
            if line == "No results were found.":
                continue
            find = re.compile(r"^[^,]*")
            name = re.search(find, line).group(0)
            print name
            wwn = re.findall(",(.*)$", line)
            wwn = wwn[0]
            wwn = re.sub(r'"wwpns=', '', wwn) 
            wwn = re.sub(r'"', '', wwn) 
            print wwn

            server_name = AIXServer.objects.get(name=name)
            AIXWorldWideName.objects.get_or_create(name=server_name, world_wide_name=wwn)

            #    pool_data = AIXProcPool.objects.get_or_create(frame=frame_obj, pool_name=pool_name, max_proc_units=max_proc_units, used_proc_units=used_proc_units, curr_procs=curr_procs, modified=timezone.now())




                        #change_message = "Server is now inactive. Set active to False"
                        #LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)
#                except:
#                    AIXServer.objects.get_or_create(name=server.rstrip(), frame=frame.rstrip(), os='AIX', active=False)



    #for server in exclusion_list:
    #    Server.objects.filter(name=server).update(exception=True)
#def add_server(name, frame, os):
#    s = Server.objects.get_or_create(name=name, fos='AIX')[0]
#    return s



#start execution
if __name__ == '__main__':
    print "Starting populations..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    populate()
