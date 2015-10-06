#UNIX Dashboard views.py

from __future__ import division #But don't tell anyone, for the sake of the world.
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from server.models import AIXServer, HistoricalAIXData
from server.models import AIXProcPool
from server.models import HistoricalAIXProcPoolData

from server.models import LinuxServer, HistoricalLinuxData
from server.models import WindowsServer #SERIOUSLY???
from server.models import Frame
from server.models import Relationships
from django.contrib.admin.models import LogEntry

import todo.models
from todo.models import ReleaseNotes

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template import RequestContext, Context

import datetime, calendar
import sys
import os
from itertools import chain

from django.db.models import Q
import operator


def get_zone(zone):
    if (zone == 'nonproduction') or (zone == '1'):
        zone = 1
        #here we're crafting the 2 subtitle urls of the other zones to link to
        zone_label1 = 'All'
        zone_label2 = 'Production'
        zone_url1 = 'all'
        zone_url2 = 'production'
        zone_title = 'NonProduction'
    elif (zone == 'production') or (zone == '2'):
        zone = 2
        zone_label1 = 'All'
        zone_label2 = 'NonProduction'
        zone_url1 = 'all'
        zone_url2 = 'nonproduction'
        zone_title = 'Production'
    else:
        zone_label1 = 'Production'
        zone_label2 = 'NonProduction'
        zone_url1 = 'production'
        zone_url2 = 'nonproduction'
        zone_title = ''
    return (zone, zone_label1, zone_label2, zone_url1, zone_url2, zone_title)



@login_required
def index(request):
    last_ten_notes = ReleaseNotes.objects.all().order_by('-created_date')[:20]
    note_list = []
    for note in last_ten_notes:
        line = str(note.created_date) + " --  " + str(note.release_note)
        note_list.append(line)
    last_ten_notes = note_list
    context = {'last_ten_notes': last_ten_notes}
    os.environ['REMOTE_USER'] = str(request.user.username)
    return render(request, 'server/index.html', context)

@login_required
def git_stats_dashboard(request):
    test = 'test'
    context = {'test': test}
    return render(request, 'server/git_stats_dashboard.html', context)

@login_required
def git_stats_ansible_dev(request):
    test = 'test'
    context = {'test': test}
    return render(request, 'server/git_stats_ansible_dev.html', context)

@login_required
def local_users(request):
    aix_servers = AIXServer.objects.filter(decommissioned=False, zone=2)
    linux_servers = LinuxServer.objects.filter(decommissioned=False, zone=2)
    server_list = list(chain(aix_servers, linux_servers))
    text = [] 
    for server in server_list:
        t = str(server.local_users).split('\n')
        for line in t:
            text.append(line)
    context = {'text': text, 'server_list': server_list}
    return render(request, 'server/local_users.txt', context)

def java(request):
    servers = AIXServer.objects.order_by('name')
    test = {}
    for server in servers:
        test[server.name] = server.java
    context = {'servers': servers, 'test': test}
    return render(request, 'server/java.html', context)

def jquerytest(request):
    first_ten_servers = AIXServer.objects.order_by('name')[:10]
    context = {'first_ten_servers': first_ten_servers}
    return render(request, 'server/jquerytest.html', context)


@login_required
def aix_server_table(request):
    servers = AIXServer.objects.filter(decommissioned=False).order_by('-name')
    server_list = []
    #for server in servers:
    #    line = str(note.created_date) + " --  " + str(note.release_note)
    #    note_list.append(line)
    #last_ten_notes = note_list
    context = {'servers': servers}
    os.environ['REMOTE_USER'] = str(request.user.username)
    return render(request, 'server/aix_server_table.html', context)

def treemap(request):
    predicted_100 = AIXServer.objects.filter(decommissioned=False, predicted_lpar_score=100)
    predicted_90 = AIXServer.objects.filter(decommissioned=False, predicted_lpar_score=90)
    predicted_80 = AIXServer.objects.filter(decommissioned=False, predicted_lpar_score=80)
    predicted_70 = AIXServer.objects.filter(decommissioned=False, predicted_lpar_score=70)
    predicted_60 = AIXServer.objects.filter(decommissioned=False, predicted_lpar_score=60)
    predicted_50 = AIXServer.objects.filter(decommissioned=False, predicted_lpar_score=50)
    predicted_40 = AIXServer.objects.filter(decommissioned=False, predicted_lpar_score=40)
    predicted_30 = AIXServer.objects.filter(decommissioned=False, predicted_lpar_score=30)
    predicted_20 = AIXServer.objects.filter(decommissioned=False, predicted_lpar_score=20)
    predicted_10 = AIXServer.objects.filter(decommissioned=False, predicted_lpar_score=10)
    context = {'predicted_100': predicted_100, 'predicted_90': predicted_90, 'predicted_80':predicted_80, 'predicted_70': predicted_70, 'predicted_60': predicted_60, 'predicted_50':predicted_50, 'predicted_40': predicted_40, 'predicted_30': predicted_30, 'predicted_20':predicted_20, 'predicted_10':predicted_10}
    return render(request, 'server/treemap.html', context)
    
def frames(request):
    frames = Frame.objects.all().exclude(name='None').order_by('name')
    count_dict = {}
    frame_dict = {}
    for frame in frames:
        server_count = AIXServer.objects.filter(decommissioned=False, frame=frame).count()
        count_dict[frame.name] = server_count
    #trying to sort them here
    sorted_frame_list = []
    test_list = []
    for key, value in sorted(count_dict.iteritems(), key=lambda (k,v): (v,k)):
        new_frame = Frame.objects.get(name=key)
        sorted_frame_list.append(new_frame)
        test_list.append(new_frame)
    sorted_frame_list.reverse()
    test_list.reverse()

    for frame in sorted_frame_list:
        server_list = AIXServer.objects.filter(decommissioned=False, frame=frame).order_by('name')
        frame_dict[frame] = server_list
    context = {'frames' : frames, 'frame_dict' : frame_dict, 'sorted_frame_list':sorted_frame_list, 'test_list': test_list}
    return render(request, 'server/frames.html', context)



def stacks(request, os, zone):
    request.GET.get('os')
    request.GET.get('zone')
   
    #Setting up the base filter
    #either prod, nonprod, or leave it out for everything
    if zone == 'nonproduction':
        zone = '1'
        filters = {'decommissioned': False, 'stack__name': 'Red', 'zone':zone}
    elif zone == 'production':
        zone = '2'
        filters = {'decommissioned': False, 'stack__name': 'Red', 'zone':zone}
    elif zone == 'all':
        filters = {'decommissioned': False, 'stack__name': 'Red'}


    red_aix_servers = []
    red_linux_servers = []
    red_windows_servers = []
   
    yellow_aix_servers = []
    yellow_linux_servers = []
    yellow_windows_servers = []
   
    green_aix_servers = []
    green_linux_servers = []
    green_windows_servers = []
   
    orange_aix_servers = []
    orange_linux_servers = []
    orange_windows_servers = []
   
    train_aix_servers = []
    train_linux_servers = []
    train_windows_servers = []
   
    config_aix_servers = []
    config_linux_servers = []
    config_windows_servers = []
   

    #Linux servers
    if (os == 'linux') or (os == 'all'):
        filters['stack__name'] = 'Red'
        red_linux_servers = LinuxServer.objects.filter(**filters).order_by('name')
        filters['stack__name'] = 'Yellow'
        yellow_linux_servers = LinuxServer.objects.filter(**filters).order_by('name')
        filters['stack__name'] = 'Green'
        green_linux_servers = LinuxServer.objects.filter(**filters).order_by('name')
        filters['stack__name'] = 'Orange'
        orange_linux_servers = LinuxServer.objects.filter(**filters).order_by('name')
        filters['stack__name'] = 'Train'
        train_linux_servers = LinuxServer.objects.filter(**filters).order_by('name')
        filters['stack__name'] = 'Config'
        config_linux_servers = LinuxServer.objects.filter(**filters).order_by('name')


    #AIX servers
    if os == 'aix' or os == 'all':
        filters['stack__name'] = 'Red'
        red_aix_servers = AIXServer.objects.filter(**filters).order_by('name')
        filters['stack__name'] = 'Yellow'
        yellow_aix_servers = AIXServer.objects.filter(**filters).order_by('name')
        filters['stack__name'] = 'Green'
        green_aix_servers = AIXServer.objects.filter(**filters).order_by('name')
        filters['stack__name'] = 'Orange'
        orange_aix_servers = AIXServer.objects.filter(**filters).order_by('name')
        filters['stack__name'] = 'Train'
        train_aix_servers = AIXServer.objects.filter(**filters).order_by('name')
        filters['stack__name'] = 'Config'
        config_aix_servers = AIXServer.objects.filter(**filters).order_by('name')

    #Windows servers
    if (os == 'windows') or (os == 'all'):
        filters['stack__name'] = 'Red'
        red_windows_servers = WindowsServer.objects.filter(**filters).order_by('name')
        filters['stack__name'] = 'Yellow'
        yellow_windows_servers = WindowsServer.objects.filter(**filters).order_by('name')
        filters['stack__name'] = 'Green'
        green_windows_servers = WindowsServer.objects.filter(**filters).order_by('name')
        filters['stack__name'] = 'Orange'
        orange_windows_servers = WindowsServer.objects.filter(**filters).order_by('name')
        filters['stack__name'] = 'Train'
        train_windows_servers = WindowsServer.objects.filter(**filters).order_by('name')
        filters['stack__name'] = 'Config'
        config_windows_servers = WindowsServer.objects.filter(**filters).order_by('name')

    #Chain them all together
    red_servers = list(chain(red_aix_servers, red_linux_servers, red_windows_servers))
    yellow_servers = list(chain(yellow_aix_servers, yellow_linux_servers, yellow_windows_servers))
    green_servers = list(chain(green_aix_servers, green_linux_servers, green_windows_servers))
    orange_servers = list(chain(orange_aix_servers, orange_linux_servers, orange_windows_servers))
    train_servers = list(chain(train_aix_servers, train_linux_servers, train_windows_servers))
    config_servers = list(chain(config_aix_servers, config_linux_servers, config_windows_servers))



    context = {'red_servers' : red_servers,
        'yellow_servers': yellow_servers,
        'green_servers': green_servers,
        'orange_servers': orange_servers,
        'train_servers': train_servers,
        'config_servers': config_servers}
    return render(request, 'server/stacks.html', context)


def wpars(request):
    context = RequestContext(request)
    relationship_list = Relationships.objects.all()
    context = {'relationships': relationship_list}
    return render(request, 'server/wpars.html', context)


#def pie(request):
#    red_servers = AIXServer.objects.filter(stack__name = 'Red').order_by('name')
#    context = {'red_servers' : red_servers}
#    return render(request, 'server/3d_pie.htm', context)

def pie_3d(request, os, zone, service):
    request.GET.get('os')
    request.GET.get('zone')
    request.GET.get('service')
    data = {}
    zone_title = zone

    zone, zone_label1, zone_label2, zone_url1, zone_url2, zone_title = get_zone(zone)



    if zone == 'all':
        predicates = [('active', True), ('decommissioned', False)]
    else:
        predicates = [('active', True), ('decommissioned', False), ('zone', zone)]

    q_list = [Q(x) for x in predicates]

    if os == 'aix':
        version_list = AIXServer.objects.filter(reduce(operator.and_, q_list)).values_list(service , flat=True).distinct()
        version_list = list(set(version_list))
        q_list = [Q(x) for x in predicates]
        total_server_count = AIXServer.objects.filter(reduce(operator.and_, q_list)).count()
    elif os == 'linux':
        version_list = LinuxServer.objects.filter(reduce(operator.and_, q_list)).values_list(service , flat=True).distinct()
        version_list = list(set(version_list))
        q_list = [Q(x) for x in predicates]
        total_server_count = LinuxServer.objects.filter(reduce(operator.and_, q_list)).count()
    else:
        sys.exit()

    for version in (version_list):
        if zone == 'all':
            predicates = [('active', True), ('decommissioned', False), (service, version)]
        else:
            predicates = [('active', True), ('decommissioned', False), ('zone', zone), (service, version)]
        q_list = [Q(x) for x in predicates]
        if os == 'aix':
            num = AIXServer.objects.filter(reduce(operator.and_, q_list)).count()
        elif os == 'linux':
            num = LinuxServer.objects.filter(reduce(operator.and_, q_list)).count()
        else:
            sys.exit()

        percentage = "{0:.1f}".format(num/total_server_count * 100)
        if service == 'zone':
            if version == 1:
                version = 'NonProduction'
            elif version == 2:
                version = 'Production'
            elif version == 3:
                version = 'Unsure'
        new_list = [str(version), percentage]
        data[version] = percentage

    title = "Current distribution of " + service + " on " + str(total_server_count) + " active " + os + " " + zone_title + " servers"
    subtitle1 = 'Production'
    name = "Percentage"
    return render(request, 'server/pie_3d.html', {'data': data, 'name': name, 'title': title, 'os':os, 'service':service, 'subtitle1':subtitle1, 'zone_label1':zone_label1, 'zone_label2':zone_label2, 'zone_url1':zone_url1, 'zone_url2':zone_url2})


def stacked_column(request, os, zone, service, period, time_range):
    request.GET.get('os')
    request.GET.get('zone')
    request.GET.get('service')
    request.GET.get('period')
    request.GET.get('time_range')
    data = {}

    #url = 'http://www.cnn.com/' + str(zone)
    #return HttpResponseRedirect(url)
    #sys(exit)

    zone, zone_label1, zone_label2, zone_url1, zone_url2, zone_title = get_zone(zone)


    if os == 'aix':
        os_label = os.upper()
    elif os == "linux":
        os_label = os.capitalize()

    title = "Historical distribution of " + service + " on " + os_label + " servers by " + period
    
    #doing this to cut down on the amount of calls to datetime
    today = datetime.date.today().strftime('%Y-%m-%d')

    #time_interval is the list of dates to gather data from, whether by day, week, month 
    time_interval = []
    #number_of_servers = []

    #interval is the offset for timedelta to get last sunday every week, every month or whatever
    interval = 0


    #Populate time_interval with the dates for the labels and queries
    time_interval.append(datetime.date.today().strftime('%Y-%m-%d'))

    if period == "day":
        day_offset = 1
    elif period == 'week':
        day_offset = int(datetime.date.today().weekday()) + 1
    else:
        day_offset = int(datetime.date.today().strftime('%d'))

    for x in range (1, (int(time_range))):
        end_date = (datetime.date.today() - datetime.timedelta(days = (day_offset + interval))).strftime('%Y-%m-%d')
        
        #####APPEND HERE#####
        time_interval.append(end_date)

        if period == 'week':
            interval = interval + 7
        elif period == 'day':
            interval = interval + 1
        elif period == 'month':
            if x == 0:
                #get the first day of the month, we're just adding today on the end of the graph here
                interval = interval + (int(datetime.date.today().strftime('%d')) )
            else:
            #this goes back and finds the first day of each of the last months in the time range and adjusts the year if it has to
            #the graph for days or weeks doesn't have to do this because it's a set 1 and 7 interval whereas days of the month vary
                my_year = int(datetime.date.today().strftime('%Y'))
                my_month = int(datetime.date.today().strftime('%m'))

                #We need to go to last year
                if (my_month - x) < 1:
                    my_year = my_year -1
                    my_month = my_month + 12
                next_month_back = calendar.monthrange(my_year, (my_month - x))[1]
                interval = interval + next_month_back
        else:
            #Not sure what to do here, 404? sys.exit?
            sys.exit()


    ################################################################
    #  Divider for gettin version list
    ################################################################

    #Here we'll go through each label date and use those to find which versions are on those specific dates
    version_list = []


    for my_date in time_interval:

        #FIXME Well crap.... I don't want this in here but I need that date to make the predicates....how...can I add it in after??
        if zone == 'all':
            predicates = [('active', True), ('decommissioned', False), ('date', my_date)]
        else:
            predicates = [('active', True), ('decommissioned', False), ('zone', zone), ('date', my_date)]

        q_list = [Q(x) for x in predicates]

        if os == 'aix':
            #FIXME
            #temp_list = HistoricalAIXData.objects.filter(active=True, decommissioned=False, date=my_date).values_list(service , flat=True).distinct()
            temp_list = HistoricalAIXData.objects.filter(reduce(operator.and_, q_list)).values_list(service , flat=True).distinct()
        elif os == 'linux':
            #temp_list = HistoricalLinuxData.objects.filter(active=True, decommissioned=False, date=my_date).values_list(service , flat=True).distinct()
            temp_list = HistoricalLinuxData.objects.filter(reduce(operator.and_, q_list)).values_list(service , flat=True).distinct()
        else:
            sys.exit()
        temp_list = list(set(temp_list)) #quick way to make sure you have all uniques
        version_list = version_list + temp_list  #add em up

    version_list = list(set(version_list))


    #################################################################
    # Divider for iterating over the versions
    ################################################################

    #Ok, this is a bit different, we're going to have to iterate over the date and push the number of servers into a list across dates
    version_counter = 0
    date_counter = 0
    my_array = [[], [], [], [], [], [], [], [], [], [], [], [], [], []]

    for version in version_list:
        for date in time_interval:
            #Using django Q objects to create a dynamic query here
            if zone == 'all':
                predicates = [('active', True), ('decommissioned', False), (service, version), ('date', date)]
            else:
                predicates = [('active', True), ('decommissioned', False), (service, version), ('zone', zone), ('date', date)]


            q_list = [Q(x) for x in predicates]

            if os == 'aix':
                num = HistoricalAIXData.objects.filter(reduce(operator.and_, q_list)).count()
            elif os == 'linux':
                num = HistoricalLinuxData.objects.filter(reduce(operator.and_, q_list)).count()


            if date_counter == 0:
                my_array[version_counter] = [num]
            else:
                my_array[version_counter].append(num)
            date_counter += 1

        #FIXME Need a proper call rather than hardcoding it
        if service == 'zone':
            if version == 1:
                version = 'NonProduction'
            elif version == 2:
                version = 'Production'
            elif version == 3:
                version = 'Unsure'
        data[version] = my_array[version_counter]
        version_counter += 1
    time_interval.reverse()


    #remove empty sets
    my_array = [x for x in my_array if x]

    #reverse each list in the list of lists (of lists in lists....AHHH!)
    for p in my_array:
            p.reverse()
        
    name = "Test Name"
    y_axis_title = 'Number of Servers'
    percentage = 0
    return render(request, 'server/stacked_column.html', {'data': data, 'name': name, 'title': title, 'y_axis_title':y_axis_title, 'version_list':version_list, 'time_interval':time_interval, 'my_array':my_array, 'os':os, 'service':service, 'zone_label1':zone_label1, 'zone_label2':zone_label2, 'zone_url1':zone_url1, 'zone_url2':zone_url2})


##################################################################
#################### Get total number of servers #################
##################################################################
def stacked_column_total(request, os, zone, service, period, time_range):
    request.GET.get('os')
    request.GET.get('zone')
    request.GET.get('service')
    request.GET.get('period')
    request.GET.get('time_range')
    data = {}

    #url = 'http://www.cnn.com/' + str(zone)
    #return HttpResponseRedirect(url)
    #sys(exit)

    zone, zone_label1, zone_label2, zone_url1, zone_url2, zone_title = get_zone(zone)


    if os == 'aix':
        os_label = os.upper()
    elif os == "linux":
        os_label = os.capitalize()

    title = "Total number of Linux and AIX servers by " + period
    
    #doing this to cut down on the amount of calls to datetime
    today = datetime.date.today().strftime('%Y-%m-%d')

    #time_interval is the list of dates to gather data from, whether by day, week, month 
    time_interval = []
    #number_of_servers = []

    #interval is the offset for timedelta to get last sunday every week, every month or whatever
    interval = 0


    #Populate time_interval with the dates for the labels and queries
    time_interval.append(datetime.date.today().strftime('%Y-%m-%d'))

    if period == "day":
        day_offset = 1
    elif period == 'week':
        day_offset = int(datetime.date.today().weekday()) + 1
    else:
        day_offset = int(datetime.date.today().strftime('%d'))

    for x in range (1, (int(time_range))):
        end_date = (datetime.date.today() - datetime.timedelta(days = (day_offset + interval))).strftime('%Y-%m-%d')
        
        #####APPEND HERE#####
        time_interval.append(end_date)

        if period == 'week':
            interval = interval + 7
        elif period == 'day':
            interval = interval + 1
        elif period == 'month':
            if x == 0:
                #get the first day of the month, we're just adding today on the end of the graph here
                interval = interval + (int(datetime.date.today().strftime('%d')) )
            else:
            #this goes back and finds the first day of each of the last months in the time range and adjusts the year if it has to
            #the graph for days or weeks doesn't have to do this because it's a set 1 and 7 interval whereas days of the month vary
                my_year = int(datetime.date.today().strftime('%Y'))
                my_month = int(datetime.date.today().strftime('%m'))

                #We need to go to last year
                if (my_month - x) < 1:
                    my_year = my_year -1
                    my_month = my_month + 12
                next_month_back = calendar.monthrange(my_year, (my_month - x))[1]
                interval = interval + next_month_back
        else:
            #Not sure what to do here, 404? sys.exit?
            sys.exit()


    ################################################################
    #  Divider for gettin version list
    ################################################################

    #Here we'll go through each label date and use those to find which versions are on those specific dates
    version_list = []


    for my_date in time_interval:

        #FIXME Well crap.... I don't want this in here but I need that date to make the predicates....how...can I add it in after??
        if zone == 'all':
            predicates = [('active', True), ('decommissioned', False), ('date', my_date)]
        else:
            predicates = [('active', True), ('decommissioned', False), ('zone', zone), ('date', my_date)]

        q_list = [Q(x) for x in predicates]

        #if os == 'aix':
        #   temp_list = HistoricalAIXData.objects.filter(reduce(operator.and_, q_list)).values_list(service , flat=True).distinct()
        #elif os == 'linux':
        #    temp_list = HistoricalLinuxData.objects.filter(reduce(operator.and_, q_list)).values_list(service , flat=True).distinct()
        #else:
        #    sys.exit()

        temp_list1 = HistoricalAIXData.objects.filter(reduce(operator.and_, q_list)).values_list(service , flat=True).distinct()
        temp_list2 = HistoricalLinuxData.objects.filter(reduce(operator.and_, q_list)).values_list(service , flat=True).distinct()
        temp_list = list(chain(temp_list1, temp_list2))

            
        temp_list = list(set(temp_list)) #quick way to make sure you have all uniques
        version_list = version_list + temp_list  #add em up

    version_list = list(set(version_list))


    #################################################################
    # Divider for iterating over the versions
    ################################################################

    #Ok, this is a bit different, we're going to have to iterate over the date and push the number of servers into a list across dates
    version_counter = 0
    date_counter = 0
    my_array = [[], [], [], [], [], [], [], [], [], [], [], [], [], []]

    for version in version_list:
        for date in time_interval:
            #Using django Q objects to create a dynamic query here
            if zone == 'all':
                predicates = [('active', True), ('decommissioned', False), (service, version), ('date', date)]
            else:
                predicates = [('active', True), ('decommissioned', False), (service, version), ('zone', zone), ('date', date)]


            q_list = [Q(x) for x in predicates]

            #if os == 'aix':
            #    num = HistoricalAIXData.objects.filter(reduce(operator.and_, q_list)).count()
            #elif os == 'linux':
            #    num = HistoricalLinuxData.objects.filter(reduce(operator.and_, q_list)).count()

            num1 = HistoricalAIXData.objects.filter(reduce(operator.and_, q_list)).count()
            num2 = HistoricalLinuxData.objects.filter(reduce(operator.and_, q_list)).count()
            num = num1 + num2


            if date_counter == 0:
                my_array[version_counter] = [num]
            else:
                my_array[version_counter].append(num)
            date_counter += 1

        #FIXME Need a proper call rather than hardcoding it
        if service == 'zone':
            if version == 1:
                version = 'NonProduction'
            elif version == 2:
                version = 'Production'
            elif version == 3:
                version = 'Unsure'
        data[version] = my_array[version_counter]
        version_counter += 1
    time_interval.reverse()


    #remove empty sets
    my_array = [x for x in my_array if x]

    #reverse each list in the list of lists (of lists in lists....AHHH!)
    for p in my_array:
            p.reverse()
        
    name = "Test Name"
    y_axis_title = 'Number of Servers'
    percentage = 0
    return render(request, 'server/stacked_column.html', {'data': data, 'name': name, 'title': title, 'y_axis_title':y_axis_title, 'version_list':version_list, 'time_interval':time_interval, 'my_array':my_array, 'os':os, 'service':service, 'zone_label1':zone_label1, 'zone_label2':zone_label2, 'zone_url1':zone_url1, 'zone_url2':zone_url2})













############################################################################
#############################################################################
###FIXME just putting this here for testing


#Historical view of our AIX Processor Pools
def column_basic_proc_pools(request, frame, pool_name, period, time_range):
    #request.GET.get('string')
    request.GET.get('period')
    request.GET.get('time_range')
    data = {}
   

    proc_pools = AIXProcPool.objects.filter(frame=frame)
    frame = Frame.objects.get(pk=frame)
    
    
    
    title = "AIX Processor Pools for " + str(frame.short_name) + " " + pool_name
    sub_title = frame.name


    pool_data = []
    months = []
    number_of_servers = []
    max_proc_units = []
    curr_procs = []
    used_proc_units = []
    interval = 0

    #time_interval is the list of dates to gather data from, whether by day, week, month
    time_interval = []

    for x in range (0, int(time_range)):

        
        if period == 'day':
            ls = (datetime.date.today() - datetime.timedelta(days = interval)).strftime('%Y-%m-%d')
        else:
            ls = (datetime.date.today() - datetime.timedelta(days = (datetime.date.today().weekday() + interval))).strftime('%Y-%m-%d')
        months.append(ls)
        if period == 'week':
            interval = interval + 7
        elif period == 'day':
            interval = interval + 1

        elif period == 'month':
            if x == 0:
                #get the first day of the month, we're just adding today on the end of the graph here
                interval = interval + (int(datetime.date.today().strftime('%d')) - 2)
            else:
                #this goes back and finds the first day of each of the last months in the time range and adjusts the year if it has to
                #the graph for days or weeks doesn't have to do this because it's a set 1 and 7 interval whereas days of the month vary
                my_year = int(datetime.date.today().strftime('%Y'))
                my_month = int(datetime.date.today().strftime('%m'))
                my_interval = x
                if (my_month - x) < 1:
                    my_year = my_year -1
                    my_month = my_month + 12
                next_month_back = calendar.monthrange(my_year, (my_month - x))[1]
                interval = interval + next_month_back
        else:
            #Not sure what to do here, 404? sys.exit?
            interval = interval + 1


        #tmp_list = [str(frame.name), str(pool.pool_name), pool.max_proc_units, pool.used_proc_units] 
        #pool_data.append(tmp_list)


        #Needed to put these in here to account for missing data. In stacked_column we could use a filter but we can't here
        try:
            max_proc_units.append(HistoricalAIXProcPoolData.objects.get(frame=frame, pool_name=pool_name, date=ls).max_proc_units)
        except:
            max_proc_units.append(0)
        try:
            curr_procs.append(HistoricalAIXProcPoolData.objects.get(frame=frame, pool_name=pool_name, date=ls).curr_procs)
        except:
            curr_procs.append(0)
        try:
            used_proc_units.append(HistoricalAIXProcPoolData.objects.get(frame=frame, pool_name=pool_name, date=ls).used_proc_units)
        except:
            used_proc_units.append(0)

    months.reverse()
    max_proc_units.reverse()
    curr_procs.reverse() 
    used_proc_units.reverse()

    y_axis_title = 'Procs'

    return render(request, 'server/column_basic_proc_pools.html', {'pool_data':pool_data, 'max_proc_units':max_proc_units, 'curr_procs':curr_procs, 'used_proc_units':used_proc_units, 'months':months, 'title':title, 'sub_title':sub_title, 'y_axis_title':y_axis_title})




def line_basic(request, os, period, time_range):
    request.GET.get('os')
    request.GET.get('period')
    request.GET.get('time_range')
    data = {}

    #The else is in case we add historical windows servers to this
    if os == 'aix':
        os_title = 'AIX'
    elif os == 'linux':
        os_title = 'Linux'
    else:
        os_title = ''


    name = "Test Name"
    title = "Number Of Active " + os_title + " Servers - Last " + time_range + " " + period + "s"

    
    months = []
    number_of_servers = []
    number_of_decoms = []
    number_of_prod = []
    number_of_non_prod = []
    interval = 1
    for x in range (0, int(time_range)):
        if period == 'day':
            ls = (datetime.date.today() - datetime.timedelta(days = interval)).strftime('%Y-%m-%d')
        else:
            ls = (datetime.date.today() - datetime.timedelta(days = (datetime.date.today().weekday() + interval))).strftime('%Y-%m-%d')
        months.append(ls)
        if period == 'week':
            interval = interval + 7
        elif period == 'day':
            interval = interval + 1

        elif period == 'month':
            if x == 0:
                #get the first day of the month, we're just adding today on the end of the graph here
                interval = interval + (int(datetime.date.today().strftime('%d')) - 2)
            else:
                #this goes back and finds the first day of each of the last months in the time range and adjusts the year if it has to
                #the graph for days or weeks doesn't have to do this because it's a set 1 and 7 interval whereas days of the month vary
                my_year = int(datetime.date.today().strftime('%Y'))
                my_month = int(datetime.date.today().strftime('%m'))
                my_interval = x
                if (my_month - x) < 1:
                    my_year = my_year -1
                    my_month = my_month + 12
                next_month_back = calendar.monthrange(my_year, (my_month - x))[1]
                interval = interval + next_month_back
        else:
            #Not sure what to do here, 404? sys.exit?
            interval = interval + 1
        
        if os == 'aix':
            number_of_servers.append(HistoricalAIXData.objects.filter(active=True, decommissioned=False, date=ls).count())
            number_of_decoms.append(HistoricalAIXData.objects.filter(decommissioned=True, date=ls).count())
            number_of_prod.append(HistoricalAIXData.objects.filter(active=True, decommissioned=False, zone_id=2 , date=ls).count())
            number_of_non_prod.append(HistoricalAIXData.objects.filter(active=True, decommissioned=False, zone=1 , date=ls).count())
        elif os == 'linux':
            number_of_servers.append(HistoricalLinuxData.objects.filter(active=True, decommissioned=False, date=ls).count())
            number_of_decoms.append(HistoricalLinuxData.objects.filter(decommissioned=True, date=ls).count())
            number_of_prod.append(HistoricalLinuxData.objects.filter(active=True, decommissioned=False, zone_id=2 , date=ls).count())
            number_of_non_prod.append(HistoricalLinuxData.objects.filter(active=True, decommissioned=False, zone=1 , date=ls).count())
        else:
            pass

    months.reverse()
    number_of_servers.reverse()
    number_of_decoms.reverse() 
    number_of_prod.reverse()
    number_of_non_prod.reverse()

    return render(request, 'server/line_basic.htm', {'data': data, 'months': months, 'number_of_servers': number_of_servers, 'number_of_decoms': number_of_decoms, 'number_of_prod': number_of_prod, 'number_of_non_prod': number_of_non_prod, 'name': name, 'title': title})


def detail(request, aixserver_name):
    #try:
    #    server = AIXServer.objects.get(pk=aixserver_name)
    #except:
    #    raise Http404
    log = LogEntry.objects.filter(object_repr=aixserver_name).order_by('-action_time')[:20]
    server = get_object_or_404(AIXServer, pk=aixserver_name)
    frame = get_object_or_404(AIXServer, pk=aixserver_name).frame
    return render(request, 'server/detail.html', {'server': server, 'log': log, 'frame': frame})



def linux_server_detail(request, server_linuxserver_id):
    return HttpResponse("Looking at linux server detail for %s." % server_linuxserver_id)

# Create your views here.
