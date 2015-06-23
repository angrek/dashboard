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
from server.models import AIXServer, AIXProcPool, Frame
import logging
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
    for frame in frames:
        #the output is throwing newlines at the end of the names for some reason
        #hence the use of rstrip below

        client = SSHClient()
        client.load_system_host_keys()

        #we've already established a connect6ion, but should put in error checking
        #FIXME
        client.connect('phmc01', username="wrehfiel", password=password)

        types = ['procpool']

        for type in types:
            #for each frame, let's get all of the HMC memory data
            command = 'lshwres -r ' + type + ' -m ' + frame.rstrip()
            #print command

            stdin, stdout, stderr = client.exec_command(command)
            pool_data = stdout.readlines()

            for line in pool_data:
                line = line.rstrip()
                if line != "The managed system does not support multiple shared processor pools.":
                    x = line.split(',')
                    if x[0] != "name=DefaultPool":
                        pool_name = x[0].rstrip()[5:]
                        max_proc_units = x[2].rstrip()[20:]
                        frame = frame.rstrip()
                        print "++++++++++++++++++++++++++++"
                        print "Frame: " + frame
                        print "---------------------------------------------------"
                        #full out put of the command, 
                        #print line.rstrip()
                        #print "-----------------------------------"
                        #name
                        print ">>" + x[0]
                        #shared_prod_pool_id
                        #print x[1]
                        #max_pool_proc_units
                        print ">>>" + x[2]
                        #curr_reserved_pool_proc_units
                        #print x[3]
                        #pend_reserved_pool_proc_units
                        #print x[4]

                        #Need to get the used proc units from power 7 table
                        used_proc_units = 200
                        frame_obj = Frame.objects.get(name=frame)

                        #FIXME uncomment both of these
                        try:
                            pool_data = AIXProcPool.objects.get(frame=frame_obj, pool_name=pool_name)
                            pool_data.max_proc_units = max_proc_units
                            pool_data.used_proc_unis = 300
                            pool_data.save()
                        except:
                            pool_data = AIXProcPool.objects.get_or_create(frame=frame_obj, pool_name=pool_name, max_proc_units=max_proc_units, used_proc_units=used_proc_units)





                        AIXServer.objects.filter(name=server.rstrip()).update(frame=frame.rstrip(), os='AIX', active=False, modified=timezone.now())
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