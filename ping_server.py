#!/home/wrehfiel/ENV/bin/python2.7
####################################################
#
# Script to ping the servers to see if they are up.
# If they are not, then set them as inactive in the
# Django Dashboard. -Boomer Rehfield 9/4/2014
#
####################################################

#server = 'p1rhrep'
import os

def ping(server):
    response = os.system("ping -c 1 " + str(server))
    return response

#ping(server)
