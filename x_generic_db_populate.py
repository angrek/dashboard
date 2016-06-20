#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Django server database population script - just random info for testing
#
# Boomer Rehfield - 8/7/2014
#
#########################################################################

import os

# these are need in django 1.7 and needed vs the django settings command
import django

django.setup()


# starting with AIX servers first
def populate():
    add_server(name="d1nim", os="AIX")
    add_server(name="u2jdpdb", os="AIX")
    add_server(name="u3webdb", os="AIX")


def add_server(name, ip_address, os, os_level):
    s = Server.objects.get_or_create(name=name, ip_address=ip_address, os=os, os_level=os_level)[0]
    return s


if __name__ == '__main__':
    print "Starting populations..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    from server.models import Server
    populate()
