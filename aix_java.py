#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve java versions. This is to just output text for now. 
#
# Boomer Rehfield - 8/7/2014
#
#########################################################################

import os
from ssh import SSHClient
from django.utils import timezone
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer, Java
import utilities
from django.contrib.admin.models import LogEntry
from multiprocessing import Pool
django.setup()


def update_server(server):

    java_version_list = Java.objects.values_list('name', flat=True)
    counter = 0
        
    if utilities.ping(server):
        
        client = SSHClient()
        if utilities.ssh(server, client):
            print "------------"
            print server
            
            command = "lslpp -l| grep -i java | awk '{print $1 $2}'"
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.readlines()
            java_text = []
            for line in output:
                print line
                java_text.append(line)
                line = line.rstrip()
                Java.objects.get_or_create(name=line)

                test_version = Java.objects.get(name=line)
                servers_java_versions = server.java.all()
                print "test version: " + str(test_version)
                print servers_java_versions
                if test_version not in servers_java_versions:
                    print "WINNNNNNNNNNNNNN"
                    server.java.add(test_version)
                    #utilities.log_change(server, 'bash', str(server.bash), str(bash_version))
                    message = "Added Java version " + str(test_version)
                    LogEntry.objects.create(action_time=timezone.now(), user_id=11 ,content_type_id=15, object_id =264, object_repr=server, action_flag=2, change_message=message)

            #We've added them all to Java and to the AIX Server
            #Now we need to go back and delete any that aren't on the server anymore

            dbs_java_versions = server.java.all()
            installed_versions = []
            for version in output:
                print "___" + version
                version = Java.objects.get(name=version.rstrip())
                installed_versions.append(version)

            for version in dbs_java_versions:
                if version not in installed_versions:
                    print str(version) + " not found. Removing from the database."
                    server.java.remove(version)

                    message = "Removed Java version " + str(version)
                    LogEntry.objects.create(action_time=timezone.now(), user_id=11 ,content_type_id=15, object_id =264, object_repr=server, action_flag=2, change_message=message)
                #if line in java_version_list:
                #    pass:
                #else:
                    #it's not in
                #    print "WINNAR"
                #    print line
                #print line

    
                #check if it exists
            #check existing value, if it exists, don't update
            #if str(java_text) != str(server.java_text):
            #    utilities.log_change(server, 'bash', str(server.bash), str(bash_version))
#
            #AIXServer.objects.filter(name=server).update(java_text=java_text)



#start execution
if __name__ == '__main__':
    print "Checking Bash versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = AIXServer.objects.filter(decommissioned=False)
    pool = Pool(30)
    pool.map(update_server, server_list)


    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

