#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# SNMP Remediation (Why there is excel in here I have no idea....)
#
# Boomer Rehfield - 5/7/2015
#
#########################################################################

import os
import re
from paramiko import SSHClient
from openpyxl import Workbook
from openpyxl.styles import Style, Font
# from openpyxl.styles import Style, PatternFill, Border, Side, Alignment, Protection, Font
from subprocess import check_output

# these are need in django 1.7 and needed vs the django settings command
import django
from django.utils import timezone

from server.models import AIXServer, LinuxServer
import utilities
django.setup()


s = Style(font=Font(name='Calibri', size=11, bold=True))

# need to put the timestamp in the filename
now = timezone.now()
timestamp = now.strftime('%m-%d-%Y')
filename = 'snmp_remediation_' + timestamp + '.xlsx'

wb = Workbook()
ws1 = wb.active
ws1.title = 'AIX'

# create le pretty headers
ws1['A1'] = 'IP Address'
ws1['B1'] = 'DNS Name'
ws1['C1'] = 'OS'
ws1['D1'] = 'SNMP ON'

ws1.column_dimensions["A"].width = 18
ws1.column_dimensions["B"].width = 16
ws1.column_dimensions["C"].width = 18
ws1.column_dimensions["D"].width = 16

list = ['A', 'B', 'C', 'D']

# to hell with writing all this out because the row dimensions are working...
for letter in list:
    cell = letter + '1'
    c = ws1[cell]
    c.style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))

d = ws1.row_dimensions[1].height = 20


def get_server_data():
    line = 1
    counter = 0

    ip_list = []
    # ok, let's get all the IP Addresses from the file and stick them in a list
    txt = open('vulnerable_snmp_servers', 'r')
    for my_line in txt.readlines():
        my_line = my_line.rstrip()
        ip_list.append(my_line)
    txt.close()

    # check dns for the hostnames
    for ip in ip_list:
        counter = counter + 1
        line = line + 1
        ns_command = 'nslookup ' + ip + ' | grep name'
        try:
            hostname = check_output(ns_command, shell=True)
        except:
            hostname = ''
        if hostname:
            hostname = hostname.split()[3]
            hostname = re.sub('.ad.wellcare.com.', '', hostname)
            hostname = re.sub('.wellcare.com.', '', hostname)
        print "ip:" + ip + " - hostname:" + hostname.rstrip()

        if AIXServer.objects.filter(name=hostname).exists():
            operating_system = 'AIX'
            server = AIXServer.objects.get(name=hostname)
            print "AIX SERVER"
        elif LinuxServer.objects.filter(name=hostname).exists():
            operating_system = 'Linux'
            server = LinuxServer.objects.get(name=hostname)
            print "LINUX SERVER....................."
        else:
            operating_system = ''

        # we'll go ahead and populate the first three fields
        cell = 'A' + str(line)
        ws1[cell] = ip

        cell = 'B' + str(line)
        ws1[cell] = hostname

        cell = 'C' + str(line)
        ws1[cell] = operating_system

        if operating_system != '':

            print server
            if utilities.ping(server):

                print 'ping good'
                client = SSHClient()
                if utilities.ssh(server, client):

                    print 'ssh good'
                    command = 'ps -ef | grep -v grep | grep -v dirsnmp | grep -v hyperic| grep -q snmp && echo Yes || echo No'
                    stdin, stdout, stderr = client.exec_command(command)
                    for y in stdout:
                        y = y.rstrip()
                        print y
                        cell = 'D' + str(line)
                        ws1[cell] = y

    # total
    # cell = 'A' + str(line + 1)
    # aix_cell = 'A' +str(aix_line + 1)
    # ws1[aix_cell] = 'Total'
    # ws2[cell] = 'Total'
    # ws1[aix_cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))
    # ws2[cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))

    # cell = 'E' + str(line + 1)
    # aix_cell = 'E' + str(aix_line + 1)
    # sum = "=SUM(E3:E" + str((line - 1)) + ")"
    # aix_sum = "=SUM(E3:E" + str((aix_line -1)) + ")"
    # print aix_sum
    # print sum
    # ws1[aix_cell] = aix_sum
    # ws2[cell] = sum
    # ws1[aix_cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))
    # ws2[cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))

    # cell = 'G' + str(line + 1)
    # aix_cell = 'G' + str(aix_line + 1)
    # sum = "=SUM(G3:G" + str((line - 1)) + ")"
    # aix_sum = "=SUM(G3:G" + str((aix_line - 1)) + ")"
    # print aix_cell
    # print aix_sum
    # ws1[aix_cell] = aix_sum
    # ws2[cell] = sum
    # ws1[aix_cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))
    # ws2[cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))

    # cell = 'H' + str(line + 1)
    # aix_cell = 'H' + str(aix_line + 1)
    # sum = "=SUM(H3:H" + str((line - 1)) + ")"
    # aix_sum = "=SUM(H3:H" + str((aix_line - 1)) + ")"
    # ws1[aix_cell] = aix_sum
    # ws2[cell] = sum
    # ws1[aix_cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))
    # ws2[cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))

    # create le pretty headers
    cell = 'A1'
    ws1[cell] = 'IP Address'
    ws1[cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))
    cell = 'B1'
    ws1[cell] = 'Hostname'
    ws1[cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))
    cell = 'C1'
    ws1[cell] = 'OS'
    ws1[cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))
    cell = 'D1'
    ws1[cell] = 'SNMP Active'
    ws1[cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))

    # c and f are just arbitrary vars right now for page one and two :\
    c.style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))
    # f.style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))

    wb.save(filename)

    command = 'echo "SNMP Remediation Report" | mutt -a "' + filename + '" -s "SNMP Remediation Report" -- boomer@wellcare.com'
    os.system(command)


if __name__ == '__main__':
    print "Getting server information..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    get_server_data()
