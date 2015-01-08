#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to storage size of each of the servers
#
# Boomer Rehfield - 10/24/2014
#
#########################################################################

import os
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer, Storage
import utilities
django.setup()



def update_server():
    #FIXME t9sandbox is DECOMMED UNTIL TIMEOUT IS FIXED!!!!!!!!!!!
    server_list = AIXServer.objects.filter(decommissioned=False).exclude(name__contains='vio')
    #server_list = AIXServer.objects.filter(name__contains='p1vio01')
    #server_list = AIXServer.objects.filter(name__contains='auto').exclude(name__contains='vio')
    server_count = AIXServer.objects.filter(decommissioned=False).exclude(name__contains='vio').count()
    counter  = 1
    for server in server_list:
        print "---------------------------------------"
        print "server " + str(counter) + " of " + str(server_count) + " ->" + str(server)
        counter += 1
            
        if utilities.ping(server):
            print 'ping good'

            client = SSHClient()
            if utilities.ssh(server, client):
                print 'ssh good'

                stdin, stdout, stderr = client.exec_command('dzdo /scripts/dashboard_disksize.sh')
                try:
                    if stderr.readlines()[0]:
                        print "ERROR!"
                        for line in stderr:
                            print len(line.rstrip())
                            print line.rstrip()
                    #FIXME - this needs to be shot out via email to me if there's an error
                    continue
                except:
                    pass

                for line in stdout:
                    print line.rstrip()
                
                #FIXME need logging to show that we added thes
                
                if Storage.objects.get(name=server):
                    print '1'
                    print str(Storage.objects.get(name=server).size).rstrip()
                    print line.rstrip()
                    if str(Storage.objects.get(name=server).size).rstrip() == line.rstrip():
                        print 'value is the same'
                        pass
                    else:
                        print 'Value exists, size different, updating'
                        Storage.objects.filter(name=server).update(size=line.rstrip())
                else:
                    Storage.objects.get_or_create(name=server, size=line.rstrip())
                    print "Value didn't exist, creating"



#start execution
if __name__ == '__main__':
    print "Storage size for each server..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    from server.models import AIXServer
    update_server()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
