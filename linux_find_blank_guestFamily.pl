#!/usr/bin/perl

# List all VM's in a specific VMware Infrastructure Cluster
# Written by: Jeremy van Doorn (jvandoorn@vmware.com)
#
# This program lists all VM's in a specific Cluster.
# It will report the name of Host and the VM in a formatted table.
# At the bottom of the table, it shows the amount of VM's and Hosts found in the Cluster.
#
# This program uses the VI Perl Tool kit, which you can download from:
# http://www.sourceforge.net/projects/viperltoolkit
#
# Version History:
# V1.0.0 - 20070417 Written by request
# v1.0.1 - 20070418 Added error-trapping for incorrect Cluster Names

########## Setting the default variables for being able to work with the VMware Webservice
#use strict;
#use warnings;
use Getopt::Long;
use Term::ANSIColor qw(:constants);
use VMware::VIRuntime;
use DBI;

########## Set your username and password and define where the VMware Web Service can be located
$username = 'AD\wrehfiel';
#@bad_servers = ();

open (FILE,  "/home/wrehfiel/.ssh/p");
#@lines = <FILE>;
while (<FILE>){
    chomp;
    $password = $_;
}


#@clusters = ('Savvis Prod UCS-Linux');
@clusters = ('Savvis Non-Prod UCS-Linux', 'Savvis Non-Prod UCS-DMZ',
            'Savvis Prod UCS-DMZ', 'Savvis Prod UCS-Linux',
            'Savvis Prod UCS-SANMGMT');
#@clusters = ('Savvis Non-Prod UCS-DMZ');
##my $cluster_name = "Savvis Non-Prod UCS-Linux";
#my $cluster_name = "Savvis Non-Prod UCS-DMZ";

foreach $cluster_name(@clusters){

if ($cluster_name =~ /Non-Prod/){
    $service_url = "https://vcenterdev01/sdk/vimService";
}else{
    $service_url = "https://vcenterprod01/sdk/vimService";
}

print $cluster_name;
########## Login to the VMware Infrastrucure Web Service
Vim::login(service_url => $service_url, user_name => $username, password => $password);

########## Get a view of the specified Cluster
my $cluster_view = Vim::find_entity_view(view_type => 'ClusterComputeResource',
                                            filter => { name => $cluster_name });

########## Error trap: verify if the cluster_view variable was set in the previous command
##########             if it was not set, the Cluster Name is incorrect
if (!$cluster_view) {
   die  "\nERROR: '" . $cluster_name . "' was not found in the VMware Infrastructure\n\n";
}

########### Print the table header
#print "\n";
#print "|--------------------------------------------------------------------------|\n";
#print "| VMware Cluster: " . $cluster_view->name . "\n"; 
#print "|--------------------------------------------------------------------------|\n";

########## Get a view of the ESX Hosts in the specified Cluster
my $host_views = Vim::find_entity_views(view_type => 'HostSystem',
                                        begin_entity => $cluster_view);

my $hostcounter = 0;
my $vmcounter = 0;

%hash_of_servers = ();

foreach my $host (@$host_views) {

  ########## Get a view of the current host
  my $host_view = Vim::find_entity_view(view_type => 'HostSystem',
                                        filter => { name => $host->name } );

  ########## Get a view of the Virtual Machines on the current host
  my $vm_views = Vim::find_entity_views(view_type => 'VirtualMachine',
                                      begin_entity => $host_view );

  ########## Print information on the VMs and the Hosts
    foreach my $vm (@$vm_views) {
        #print "==============================================================";
        #print "\nName--->", $vm->name;
        #print "\nguestFamily--->", $vm->guest->guestFamily;
        #print "\nguestFullName->", $vm->guest->guestFullName;
        #print "\nguestState---->", $vm-guest-guestState;
        #print "\nCluster name-->", $cluster_name;
        #print "\nHost --------->", $host;

        if (($vm->guest->guestFamily) eq ''){
            #push (@bad_servers, $vm->name);
            print "==============================================================";
            print "\nName--->", $vm->name;
            print "\nguestFamily--->", $vm->guest->guestFamily;
            print "\nguestFullName->", $vm->guest->guestFullName;
            print "\nguestState---->", $vm-guest-guestState;
            print "\nCluster name-->", $cluster_name;
            print "\nHost --------->", $host;
        } 

        
        #FIXME broken for testing! FIX NOW!
        if ((($vm->guest->guestFamily) eq 'linuxGueist') || (($vm-name) eq 'p1dbmon')){


            $tmp = ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst)=localtime(time);
            $timestamp = sprintf ("%04d-%02d-%02d %02d:%02d:%02d",
                                    $year+1900,$mon+1,$mday,$hour,$min,$sec);


            #putting it into an array
            $server_name=$vm->name;
            $esx_server_name = $host->name;
            $guest_family = $vm->guest->guestFamily;
            $state = $vm->guest->guestState;
            $memory = $vm->runtime->maxMemoryUsage;
            $cpu = $vm->summary->config->numCpu;
            $active = '';

            #ORM apparently isn't liking NULL....
            if ($memory == ''){$memory = 0;}
            if ($cpu == ''){$cpu = 0;}


            if ($state eq 'running'){
                $active = True;
            }else{
                $active = False;
            }

            #it can be inactive with an ip,lets grab it from  nslookup
            $ns_command = "nslookup $server_name | grep Address | grep -v '#'";
            $ip_address = qx($ns_command);
            $ip_address = substr $ip_address, 9, -1;

            if ($ip_address == ''){
                $ipaddress = "0.0.0.0";
            }

            #setting exception to true. The SSH keys script runs after this script
            #and should pick it up, transfer keys, and then the first script will switch the exception.
            $exception = 1;



            $dbh = DBI->connect('DBI:mysql:dashboard', 'wrehfiel', '') || die "Could not connect to database: $DBI::errstr";
            $rv=$dbh->do("lock table server_linuxserver write");
            $sth = $dbh->prepare (qq{insert into server_linuxserver (
                name,
                vmware_cluster,
                active,
                exception,
                created,
                modified,
                ip_address,
                zone_id,
                memory,
                cpu)
                VALUES (?,?,?,?,?,?,?,?,?,?) ON DUPLICATE KEY UPDATE vmware_cluster="$cluster_name", active=$active, exception=$exception, modified="$timestamp", ip_address="$ip_address",  memory=$memory, cpu=$cpu} );
            $sth->execute($server_name, $cluster_name, $active, $exception, "$timestamp", "$timestamp", "$ip_address", 3, $memory, $cpu);
            $rv=$dbh->do("unlock table");
            $dbh->disconnect();


            $vmcounter++;

            #LEAVE THIS HERE TO SEE VALUES FOR THE FUTURE
            #Dumper command to get all of the possible data we can pull out of ESX 
            #if ($vmcounter == 5){
            #     print Dumper($vm);
            #     break;
            #}
        } 
    }

    $hostcounter++;
}
}

Vim::logout();
#print "Bad servers:";
#foreach $baddy(@bad_servers){
#    print "\n$baddy";
#}
