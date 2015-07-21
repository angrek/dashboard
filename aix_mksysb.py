#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to make sure our mksysb's are up to date
#
# Boomer Rehfield - 1/13/2015
#
#########################################################################

import os, sys, re
from subprocess import *
from time import strptime
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer, Relationships
import utilities
from  datetime import datetime, date, timedelta
import datetime
django.setup()


def get_a_good_server(zone):
    #I'm banking that five servers won't be missing the /mksysb directory all at the same time....
    server_list = AIXServer.objects.filter(active=True, decommissioned=False, zone=zone)
    success = 0
    
    for server in server_list:
        if utilities.ping(server):
            client = SSHClient()
            if utilities.ssh(server, client):
                stdin, stdout, stderr = client.exec_command(' [ -d /mksysb/ ] && echo 1 || echo 0')
                test = stdout.readlines()
                if int(test[0]):
                    success = 1
                    break
    if not success:
        subject = 'None of the servers have a /mksysbWPAR directory'
        print subject
        utilities.send_email(subject, server_list)
        sys.exit()
    else:
        return server


def update_server():
    count = 0
    zone=1
    nonprod_base_server = get_a_good_server(zone)
    zone=2
    prod_base_server = get_a_good_server(zone)

    main_server_list = AIXServer.objects.filter(active=True, decommissioned=False)

    #PRODUCTION
    #get the dir listing for /mksysb
    main_command = 'ssh ' + prod_base_server.name + ' ls -lp /mksysb | grep mksysb | grep -v /'
    p = Popen(main_command, shell=True, stdout=PIPE)
    p.wait()
    prod_main_directory_list = p.stdout.readlines()

    #get the dir listing for /mksysb
    main_command = 'ssh ' + nonprod_base_server.name + ' ls -lp /mksysb | grep mksysb | grep -v /'
    p = Popen(main_command, shell=True, stdout=PIPE)
    p.wait()
    main_directory_list = p.stdout.readlines()

    #get the dir listing for /mksysb/VIOS
    vios_command = 'ssh ' + nonprod_base_server.name + ' ls -lp /mksysb/VIOS | grep -v log | grep -v total | grep -v /'
    p = Popen(vios_command, shell=True, stdout=PIPE)
    p.wait()
    vios_directory_list = p.stdout.readlines()
    #print vios_directory_list

    #get the dir listing for /mksysb/WPARS
    wpars_command = 'ssh ' + nonprod_base_server.name + ' ls -lp /mksysb/WPARS | grep bak | grep -v /'
    p = Popen(wpars_command, shell=True, stdout=PIPE)
    p.wait()
    wpars_directory_list = p.stdout.readlines()

    main_directory_list += prod_main_directory_list



    #these are lists of mksysb entries from the directories of good mksysbs to add
    yesterdays_list = [] 
    todays_list = [] 
    old_list = []
    old_dict = {} 
    #we are iterating over every mksysb rather than every server because
    #we care more about what entries there are.
    def get_dir_lists(list, count):
        for entry in list:
           
            #NOTO: key will have to be the hostname. If there are duplicates,
            #we will need to get those first, set the duplicates flag, check
            #if they exist in the database and create if not, and then ditch
            #them so they don't screw up the dict

            #also of note, I'm really only looking for one mksysb per day
            #if 2 were created on the same day, it doesn't really matter, it exists
            #we DO care if it was created midday and not picked up at the 4am run
            test = entry.rstrip().split()
            filename = test[8]
           
            #These are the good ones
            #today = str(datetime.date.today())
            #yesterday = str(datetime.date.today() - timedelta(1))

            #FIXME pretending it's Monday
            today = str(datetime.date.today())
            yesterday = str(datetime.date.today() - timedelta(1))


            #month from ls is in text and we need to convert it for the timestamp
            month = str(strptime(test[5], '%b').tm_mon)

            #need one without the zero also to compare below
            temp_month = month
            if len(month) == 1:
                month = '0' + month

            if len(test[6]) == 1:
                day = '0' + test[6]
            else:
                day = test[6]
            date = month + '-' + day 


            #*nix listings are in time, unless it's last year then it lists the
            #year instead so we need to find the : to determine which it is
            timestamp = test[7]
            if re.match('..:..', timestamp, flags=0):
                #This means the timestamp is within the last 6 months
                our_month = datetime.date.today().month
                #print 'our month .' + str(our_month) + '.'
                #print 'temp month .' + str(temp_month) + '.'
                if int(temp_month) <= int(our_month):
                    year = '2015'
                else:
                    year = '2014'
            else:
                year = timestamp
            datestamp = year + '-' + date



            #FIXME take out looking for mksysb from 2 days ago, just for testing!!!
            #print 'BINGO'
            #print filename
            #print datestamp
            if datestamp == today:
                todays_list.append(filename.split('.')[0])
                count += 1
            elif datestamp == yesterday:
                yesterdays_list.append(filename.split('.')[0])
                count += 1
            else:
                old_list.append(filename.split('.')[0])
                count += 1
                old_dict[filename.split('.')[0]] = datestamp
        #print 'count = ' + str(count)    

    #lets get the all the lists now
    get_dir_lists(main_directory_list, count)
    get_dir_lists(vios_directory_list, count)
    get_dir_lists(wpars_directory_list, count)
    all_directory_list = main_directory_list + vios_directory_list + wpars_directory_list

    #we really only need this list on Monday morning for Sunday fails
    #FIXME CHange email to Monday
    if datetime.date.today().strftime("%A") == 'Monday':
        sorted = old_dict.items()
        sorted.sort()
        message = ''
        for x,y in sorted:
            message = message + x + ' - ' + y + ' \n'

        utilities.send_email('Old Mksysb files', message)

    #print 'today----------------------'
    #print todays_list
    #print 'yesterday-------------------------'
    #print yesterdays_list
    #print 'OLD-------------------------'
    #print old_list
    #print 'COUNT======================'
    #print count
    #print
    #print timestamp 
    #FIXME - for now I'm leaving out the timestamp but may want it later in the model



    #main_server_list = []
    for server in main_server_list:
        success = 0
        for entry in all_directory_list:
            test = entry.rstrip().split()
            filename = test[8].split('.')[0]
            #print server.name
            #print filename
            if server.name == filename:
                print server.name + ' is good'
                success = 1
                continue
        if success == 0:
            print server.name + 'FAILED!!!!!!!!!'

    #print main_directory_list

    #    
    #    if re.match('vio', server.name):
    #    if server.name in vio_server_list:
    #        print server.name + " is a vio server."
    #        if server.name in vios_directory:
    #            print 'YES!!'
    #    elif server.name in wpar_server_list:
    #        print server.name + " is a WPAR."
    #    else:
    #        print server.name



#start execution
if __name__ == '__main__':
    print "Checking Mksysb versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

