#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to get centrify version from the Linux servers and drop it into Django dashboard
#
# Boomer Rehfield - 11/13/2014
#
#########################################################################

import os
from ssh import SSHClient
from django.utils import timezone
from django.contrib.admin.models import LogEntry
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer, Zone
import ping_server
django.setup()



def update_server():
    server_list = AIXServer.objects.all()
    #just a quick way to on off test a server without the whole list
    #server_list = AIXServer.objects.filter(name='ustswebdb')
    for server in server_list:
        server_is_active=1
        new_centrify = ''

        #these are hardcoded because
        #none of the vio servers have Centrify installed on them
        server_exceptions = AIXServer.objects.filter(name__contains='vio')

        #Make sure the server is set to active and not an exception
        if AIXServer.objects.filter(name=server, active=True, exception=False) and str(server) not in server_exceptions:
            response = ping_server.ping(server)
            
            #typically = is false, but that's what ping gives back for a positive
            if response == 0:
                client = SSHClient()
                client.load_system_host_keys()

                #without try, it will break the script if it can't SSH
                try:
                    client.connect(str(server), username="wrehfiel")
                except:
                    #print 'SSH to ' + str(server) + ' failed, changing exception'
                    AIXServer.objects.filter(name=server).update(exception=True, modified=timezone.now())

                    #LogEntry.objects.create(action_time='2014-08-25 20:00:00', user_id=11, content_type_id=9, object_id =264, object_repr=server, action
                    LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='SSH failed, changed exception.')
                    server_is_active=0

                if server_is_active:
                    centrify_is_installed = 1
                    stdin, stdout, stderr = client.exec_command('adinfo -v')
                    try:
                        centrify = stdout.readlines()[0]
                        new_centrify = centrify[8:-2]
                    except:
                        new_centrify = "Not Installed"
                        centrify_is_installed = 0

                    #if it's the same version, we don't need to update the record
                    if str(new_centrify) != str(server.centrify):
                        old_version = str(server.centrify)
                        AIXServer.objects.filter(name=server, exception=False, active=True).update(centrify=new_centrify)
                        AIXServer.objects.filter(name=server, exception=False, active=True).update(modified=timezone.now())
                        change_message = 'Changed Centrify version from ' + old_version + ' to ' + str(new_centrify) + '.' 
                        LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)
                    if centrify_is_installed:
                        #Since we're using adinfo to find the zone, it fits that it should be here in the centrify script
                        stdin, stdout, stderr = client.exec_command('adinfo | grep Zone')
                        #print stdout.readlines()[0]
                        x = stdout.readlines()[0].split("/")
                        zone_tmp = x[4].rstrip()
                        zone = Zone.objects.get(name=zone_tmp)

                        AIXServer.objects.filter(name=server, exception=False, active=True).update(zone=zone)
                    
            else:
                AIXServer.objects.filter(name=server).update(active=False)
                #print str(server) + ' not responding to ping, setting to inactive.'
                AIXServer.objects.filter(name=server, exception=False, active=True).update(modified=timezone.now())
                LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='Ping failed, changed to inactive.')




#start execution
if __name__ == '__main__':
    print "Checking centrify version..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    from server.models import AIXServer
    update_server()
    elapsed_time= timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
