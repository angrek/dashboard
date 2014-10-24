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


########## Set your username and password and define where the VMware Web Service can be located
my $username = 'AD\wrehfiel';
#my $service_url = "https://172.28.1.250/sdk/vimService";
#my $service_url = "https://vcenterdev01:9443/sdk/vimService";
my $service_url = "https://vcenterdev01/sdk/vimService";
#my $service_url = "https://esx028/sdk/vimService";

my $cluster_name = "Savvis Non-Prod UCS-Linux";


open (FILE,  "/home/wrehfiel/.ssh/p");
#@lines = <FILE>;
while (<FILE>){
    chomp;
    $password = $_;
}


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

########## Print the table header
print "\n";
print "|--------------------------------------------------------------------------|\n";
print "| VMware Cluster: " . $cluster_view->name . "\n"; 
print "|--------------------------------------------------------------------------|\n";

########## Get a view of the ESX Hosts in the specified Cluster
my $host_views = Vim::find_entity_views(view_type => 'HostSystem',
                                        begin_entity => $cluster_view);

my $hostcounter = 0;
my $vmcounter = 0;
foreach my $host (@$host_views) {

  ########## Get a view of the current host
  my $host_view = Vim::find_entity_view(view_type => 'HostSystem',
                                        filter => { name => $host->name } );

  ########## Get a view of the Virtual Machines on the current host
  my $vm_views = Vim::find_entity_views(view_type => 'VirtualMachine',
                                      begin_entity => $host_view );

  ########## Print information on the VMs and the Hosts
    foreach my $vm (@$vm_views) {
      $vmcounter++;
      print "| ";
      printf '%3.3s', $vmcounter;
      print ": ";
      printf '%30.30s', $host->name;
      print " | ";
      printf '%35.35s', $vm->name;
      print " | ";
      #printf $vm->config.guestFullName;
      print $vm->guest->guestFullName;
      print "\n";
      if ($vmcounter == 5){
      #     print Dumper($vm);
           break;
      } 
    }

  $hostcounter++;
}

########## Print the table footer
print "|--------------------------------------------------------------------------|\n";
print "| Found " . $vmcounter . " Virtual Machines on " . $hostcounter . " ESX Host(s) in " . $cluster_view->name . "\n";
print "|--------------------------------------------------------------------------|\n";
print "\n";

print "\ntesting\n";
print Dumper($vm);
########## Logout of the VMware Infrastructure Web Service
Vim::logout();

