#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to go through the local passwd file and compare it against
# Centrify to see if the user even exists in the zone so we can
# get rid of all local users eventually.
#
# Boomer Rehfield - 3/15/2016
#
#########################################################################

import os
import paramiko

# these are need in django 1.7 and needed vs the django settings command
import django
from django.utils import timezone

from server.models import LinuxServer, AIXServer
import utilities
django.setup()


def update_server():

    standard_users = ['root', 'bin', 'daemon', 'adm', 'lp', 'sync', 'shutdown',
                      'halt', 'mail', 'news', 'uucp', 'operator', 'games', 'gopher',
                      'ftp', 'nobody', 'nscd', 'vcsa', 'pcap', 'rpc', 'mailnull',
                      'smmsp', 'rpcuser', 'nfsnobody', 'sshd', 'ntp', 'dbus', 'avahi',
                      'haldaemon', 'xfs', 'avahi-autoipd', 'gdm', 'sabayon', 'nagios',
                      'apache', 'HMC_Backup', 'hyperic', 'csi_acct', 'nxmon', 'mysql',
                      'oprofile', 'ganglia', 'nslcd', 'postfix', 'tcpdump', 'oracle',
                      'squid', 'tomcat', 'saslauth', 'pegasus', 'abrt', 'webalizer',
                      'postgres', 'cimsrvr', 'qpidd', 'mqm', 'wcapp', 'git', 'rpm',
                      'distcache', 'esbapp', 'svcitops', 'casapp', 'jboss', 'alfresco',
                      'haproxy', 'websvc', 'splunk', 'hadoop', 'puppet', 'yarn', 'hive',
                      'ambari-qa', 'hcat', 'hdfs', 'mapred', 'zookeeper', 'micsvc', 'mongodb',
                      'informatica', 'dynatrace', 'rrdcached', 'dockerroot', 'redmine',
                      'systemd-bus-proxy', 'systemd-network', 'jenkins', 'named', 'oracle9i',
                      'oraagent', 'hacluster', 'admin', 'anm-mysql', 'jira', 'chrony',
                      'unbound', 'tss', 'polkitd', 'rundeck', 'content', 'hbase', 'oozie',
                      'storm', 'falcon', 'tez', 'sqoop', 'pwrsvc', 'flume', 'ams', 'accumulo',
                      'httpfs', 'ranger', 'spark', 'prodctrl', 'gpadmin', 'memcached',
                      'amanda', 'piranha', 'webadmin', 'fax', 'mailman', 'exim', 'ldap'
                      'autosys', 'marklogic', 'rangerlogger', 'rangeradmin', 'attunity',
                      'AGMPRDSVC', 'foreman', 'elasticsearch', 'foreman-proxy', 'gutterball',
                      'qdrouterd', 'kickstart', 'nocpulse', 'protect', 'tunnel', 'arcsightsvc',
                      'stunnel', 'hue', 'xasecure', 'appviewx', 'anm', 'quest', 'nxpgsql',
                      'lpar2rrd', 'cacti', 'ucmbackup', 'sungard', 'rmsvc', 'jabber', 'pwrsvcrm',
                      'autosys', 'cca_dev_', 'rstudio', 'rstudio-server', 'rrdcache', 'iteraplan',
                      'service', 'db2inst1', 'db2fenc1', 'dasusr1', 'lsfadmin']

    server_list = AIXServer.objects.filter(decommissioned=False, active=True, zone=2)
    # server_list = LinuxServer.objects.filter(name__contains='p1rhrep')

    main_user_count = 0
    server_count = 0

    for server in server_list:

        if utilities.ping(server):

            client = paramiko.SSHClient()
            if utilities.ssh(server, client):

                #Get all local users and filter against the standard_users dict
                server_count = server_count + 1

                command = "dzdo cat /etc/passwd"
                stdin, stdout, stderr = client.exec_command(command)
                counter = 0
                local_users = []

                for line in stdout.readlines():

                    name = line.split(':')[0].rstrip()
                    if name in standard_users:
                        continue
                    else:
                        local_users.append(name)

                for name in local_users:

                    main_user_count = main_user_count + 1
                    counter = counter + 1

                    if counter == 1:
                        print "                                      "
                        print "======================================"
                        print server.name + " - Unknown Local Users"
                        print "======================================"
                    command = "adquery user -e " + name
                    stdin, stdout, stderr = client.exec_command(command)

                    try:
                        output = stdout.readlines()[0].rstrip()
                        print name + " -> " + output
                    except:
                        output = stderr.readlines()[0].rstrip()
                        print name + " -> " + output

                #Get active directory/Centrify users        
                #command = "adquery user"
                #stdin, stdout, stderr = client.exec_command(command)

                #print "======================================"
                #print server.name + " - Users via Centrify"
                #print '-------------------'

                #for line in stdout.readlines():
                #    print line.rstrip()
    print ""
    print ""
    print "======================================"
    print "======================================"
    print "Number of Servers:     " + str(server_count)
    print "Number of Local Users: " + str(main_user_count)
    print "======================================"


if __name__ == '__main__':
    print "Production User Access Report"
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
