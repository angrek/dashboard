#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# EMC AIX server information report. This is for all network connections
#
# Boomer Rehfield - 5/7/2015
#
#########################################################################

import os
import re
from subprocess import call
from ssh import SSHClient
from openpyxl import Workbook
from openpyxl.styles import Style, PatternFill, Border, Side, Alignment, Protection, Font

from django.utils import timezone
from server.models import AIXServer, LinuxServer, Power7Inventory, Storage

import utilities

#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
django.setup()


s = Style(font=Font(name='Calibri', size=11, bold=True))

#need to put the timestamp in the filename
now = timezone.now()
timestamp = now.strftime('%m-%d-%Y')
filename = 'all_network_conections' + timestamp + '.xlsx'


wb = Workbook()
ws1 = wb.active
ws1.title = 'AIX'


#create le pretty headers
ws1['A1'] = 'local_ip_addr'
ws1['B1'] = 'local_port'
ws1['C1'] = 'remote_ip_addr'
ws1['D1'] = 'remote_port'
ws1['E1'] = 'protocol'
ws1['F1'] = 'state'
ws1['G1'] = 'uid'
ws1['H1'] = 'pid'
ws1['I1'] = 'cmd'


ws1.column_dimensions["A"].width = 20
ws1.column_dimensions["B"].width = 16
ws1.column_dimensions["C"].width = 20
ws1.column_dimensions["D"].width = 16
ws1.column_dimensions["E"].width = 20
ws1.column_dimensions["F"].width = 20
ws1.column_dimensions["G"].width = 20
ws1.column_dimensions["H"].width = 20
ws1.column_dimensions["I"].width = 150

list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

#to hell with writing all this out because the row dimensions are working...
for letter in list:
    cell = letter + '1'
    c = ws1[cell]
    c.style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))

d = ws1.row_dimensions[1].height = 20

def get_server_data():
    line = 1
    counter = 0
    server_list = AIXServer.objects.filter(active=True, exception=False, decommissioned=False).exclude(name__contains='sas').exclude(name__contains='spds')

    for server in server_list:
        print server.name

        if utilities.ping(server):
            
            print 'ping good'
            client = SSHClient()
            if utilities.ssh(server, client):
                
                print 'ssh good'

                counter = counter + 1

                command = "netstat -An"
                stdin, stdout, stderr = client.exec_command(command)

                output = stdout.readlines()


                for row in output:
                    line = line + 1
                    if re.search('Active UNIX', row):
                        line = line - 1
                        break
                    if re.search('Active', row):
                        line = line - 1
                        continue
                    if re.search('PCB', row):
                        line = line - 1
                        continue

                    if row.rstrip():
                        print '>' + row.rstrip()
                        row = row.split()
                        protocol = row[1]
                        print 'Protocol:' + protocol

                        #these are giving issues for now
                        if protocol == 'tcp6':
                            line = line - 1
                            continue
                        if protocol == 'udp6':
                            line = line - 1
                            continue
                        local_address = row[4]
                        if local_address == '*.*':
                            local_port = ''
                        else:
                            local_port = local_address.split('.')[4]
                            x = local_address.split('.')
                            local_address = x[0] + '.' + x[1] + '.' + x[2] + '.' + x[3]
                        print 'Local Address: ' + local_address
                        print 'Local Port:' + local_port

                        remote_address = row[5]
                        if remote_address == '*.*':
                            remote_port = ''
                        else:
                            remote_port = remote_address.split('.')[4]
                            x = remote_address.split('.')
                            remote_address = x[0] + '.' + x[1] + '.' + x[2] + '.' + x[3]
                        print 'Remote Address: ' + remote_address
                        print 'Remote Port: ' + remote_port

                        try:
                            state = row[6]
                            print 'State:' + state
                        except:
                            state = ''
                            print 'State not shown'

                        socket = row[0]
                        command = "rmsock " + socket + " tcpcb"
                        stdin, stdout, stderr = client.exec_command(command)
                        try:
                            pid = stdout.readlines()[0]
                        except:
                            pid = ''

                        if re.search('proccess', pid):
                            pid = pid.split()[8]
                        else:
                            pid = ''
                        print pid

                        command = "ps -ef | grep " + pid + " | grep -v grep"
                        stdin, stdout, stderr = client.exec_command(command)
                        try:
                            out = stdout.readlines()[0].split()[0]
                        except:
                            out = ''

                        print out
                        uid = ''
                        if out:
                            command = "id -u " + out
                            stdin, stdout, stderr = client.exec_command(command)
                            try:
                                uid = stdout.readlines()[0].rstrip()
                            except:
                                uid = 0
                        print uid

                        command = "ps -o args -p " + pid
                        stdin, stdout, stderr = client.exec_command(command)
                        try:
                            cmd = stdout.readlines()[1].rstrip()
                        except:
                            cmd = ''

                        print cmd

                        cell = 'A' + str(line)
                        ws1[cell] = local_address

                        cell = 'B' + str(line)
                        ws1[cell] = local_port

                        cell = 'C' + str(line)
                        ws1[cell] = remote_address

                        cell = 'D' + str(line)
                        ws1[cell] = remote_port

                        cell = 'E' + str(line)
                        ws1[cell] = protocol

                        cell = 'F' + str(line)
                        ws1[cell] = state

                        cell = 'G' + str(line)
                        ws1[cell] = uid

                        cell = 'H' + str(line)
                        ws1[cell] = pid

                        cell = 'I' + str(line)
                        ws1[cell] = cmd


        




    #total
    #cell = 'A' + str(line + 1)
    #aix_cell = 'A' +str(aix_line + 1)
    #ws1[aix_cell] = 'Total'
    #ws2[cell] = 'Total'
    #ws1[aix_cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))
    #ws2[cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))
#
    #cell = 'E' + str(line + 1)
    #aix_cell = 'E' + str(aix_line + 1)
    #sum = "=SUM(E3:E" + str((line - 1)) + ")"
    #aix_sum = "=SUM(E3:E" + str((aix_line -1)) + ")"
    #print aix_sum
    #print sum
    #ws1[aix_cell] = aix_sum
    #ws2[cell] = sum
    #ws1[aix_cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))
    #ws2[cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))
#
    #cell = 'G' + str(line + 1)
    #aix_cell = 'G' + str(aix_line + 1)
    #sum = "=SUM(G3:G" + str((line - 1)) + ")"
    #aix_sum = "=SUM(G3:G" + str((aix_line - 1)) + ")"
    #print aix_cell
    #print aix_sum
    #ws1[aix_cell] = aix_sum
    #ws2[cell] = sum
    #ws1[aix_cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))
    #ws2[cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))

    #cell = 'H' + str(line + 1)
    #aix_cell = 'H' + str(aix_line + 1)
    #sum = "=SUM(H3:H" + str((line - 1)) + ")"
    #aix_sum = "=SUM(H3:H" + str((aix_line - 1)) + ")"
    #ws1[aix_cell] = aix_sum
    #ws2[cell] = sum
    #ws1[aix_cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))
    #ws2[cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))

#create le pretty headers
    cell = 'A1'
    ws1[cell] = 'local_ip_addr'
    ws1[cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))
    cell = 'B1'
    ws1[cell] = 'local_port'
    ws1[cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))
    cell = 'C1'
    ws1[cell] = 'remote_ip_addr'
    ws1[cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))
    cell = 'D1'
    ws1[cell] = 'remote_port'
    ws1[cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))
    cell = 'E1'
    ws1[cell] = 'protocol'
    ws1[cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))
    cell = 'F1'
    ws1[cell] = 'state'
    ws1[cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))
    cell = 'G1'
    ws1[cell] = 'uid'
    ws1[cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))
    cell = 'H1'
    ws1[cell] = 'pid'
    ws1[cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))
    cell = 'I1'
    ws1[cell] = 'cmd'
    ws1[cell].style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))




    #c and f are just arbitrary vars right now for page one and two :\
    c.style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))
    #f.style = Style(font=Font(name='Arial', size=11, bold=True, vertAlign=None, color='FF000000'))

    command = 'echo "Unix Configuration Report" | mutt -a "' + filename + '" -s "Unix Configuration Report" -- boomer@wellcare.com'
    os.system(command)


    wb.save(filename)





#start execution
if __name__ == '__main__':
    print "Getting server information..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    get_server_data()

    #print "Elapsed time: " + str(elapsed_time)







