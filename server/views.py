#UNIX Dashboard views.py

from __future__ import division #But don't tell anyone, for the sake of the world.
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.http import HttpResponse
from server.models import AIXServer, HistoricalAIXData
#from server.models import AIXServer, LinuxServer, Relationships, HistoricalAIXData, HistoricalLinuxData

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template import RequestContext, Context

import datetime, calendar
import sys

from django.db.models import Q
import operator
     
def index(request):
    first_ten_servers = AIXServer.objects.order_by('name')[:10]
    context = {'first_ten_servers': first_ten_servers}
    return render(request, 'server/index.html', context)

def stacks(request):
    red_servers = AIXServer.objects.filter(stack__name = 'Red', decommissioned=False).order_by('name')
    yellow_servers = AIXServer.objects.filter(stack__name = 'Yellow', decommissioned=False).order_by('name')
    green_servers = AIXServer.objects.filter(stack__name = 'Green', decommissioned=False).order_by('name')
    orange_servers = AIXServer.objects.filter(stack__name = 'Orange', decommissioned=False).order_by('name')
    #server_list = AIXServer.objects.filter(stack__name ='Red')
    context = {'red_servers' : red_servers,
        'yellow_servers': yellow_servers,
        'green_servers': green_servers,
        'orange_servers': orange_servers}
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
    if zone == 'nonproduction':
        zone = '1'
    elif zone == 'production':
        zone = '2'

    if zone == 'all':
        predicates = [('active', True), ('decommissioned', False)]
    else:
        predicates = [('active', True), ('decommissioned', False), ('zone', zone)]

    q_list = [Q(x) for x in predicates]
    version_list = AIXServer.objects.filter(reduce(operator.and_, q_list)).values_list(service , flat=True).distinct()
    #version_list = AIXServer.objects.filter(active=True, decommissioned=False).values_list(service , flat=True).distinct()
    version_list = list(set(version_list))

    q_list = [Q(x) for x in predicates]
    total_server_count = AIXServer.objects.filter(reduce(operator.and_, q_list)).count()

    for version in (version_list):
        if service == 'aix_ssh':
            if zone == 'all':
                predicates = [('active', True), ('decommissioned', False), (service, version)]
            else:
                predicates = [('active', True), ('decommissioned', False), ('zone', zone), (service, version)]
            q_list = [Q(x) for x in predicates]
            num = AIXServer.objects.filter(reduce(operator.and_, q_list)).count()
            #num = AIXServer.objects.filter(active=True, decommissioned=False, aix_ssh=version).count()
        elif service == 'cent_ssh':
            num = AIXServer.objects.filter(active=True, decommissioned=False, cent_ssh=version).count()
        elif service == 'os_level':
            num = AIXServer.objects.filter(active=True, decommissioned=False, zone='2', os_level=version).count()
        elif service == 'centrify':
            num = AIXServer.objects.filter(active=True, decommissioned=False, centrify=version).count()
        elif service == 'xcelys':
            num = AIXServer.objects.filter(active=True, decommissioned=False, xcelys=version).count()
        elif service == 'bash':
            num = AIXServer.objects.filter(active=True, decommissioned=False, bash=version).count()
        elif service == 'ssl':
            num = AIXServer.objects.filter(active=True, decommissioned=False, ssl=version).count()
        elif service == 'imperva':
            num = AIXServer.objects.filter(active=True, decommissioned=False, imperva=version).count()
        elif service == 'netbackup':
            num = AIXServer.objects.filter(active=True, decommissioned=False, netbackup=version).count()

        percentage = "{0:.1f}".format(num/total_server_count * 100)
        new_list = [str(version), percentage]
        data[version] = percentage

    if zone != 'production' or zone != 'nonproduction':
        zone = ''
    title = "Current distribution of " + service + " on " + str(total_server_count) + " " + os + " " + zone + " servers"
    name = "Percentage"
    return render(request, 'server/pie_3d.htm', {'data': data, 'name': name, 'title': title})


def stacked_column(request, os, zone, service, period, time_range):
    request.GET.get('os')
    request.GET.get('zone')
    request.GET.get('service')
    request.GET.get('period')
    request.GET.get('time_range')
    data = {}

    temp_os = os.upper()
    title = "Historical distribution of " + service + " on " + temp_os + " servers by " + period
    
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

    #Here we'll go through each label date and use those to find which versions are on those specific dates
    version_list = []
    for my_date in time_interval:
        if os=='aix':
            t = HistoricalAIXData.objects.filter(active=True, decommissioned=False, date=my_date).values_list(service , flat=True).distinct()
        elif os == 'linux':
            t = HistoricalLinuxData.objects.filter(active=True, decommissioned=False, date=my_date).values_list(service , flat=True).distinct()

        t = list(set(t))
        version_list = version_list + t
    version_list = list(set(version_list))


    #Ok, this is a bit different, we're going to have to iterate over the date and push the number of servers into a list across dates
    version_counter = 0
    date_counter = 0
    my_array = [[], [], [], [], [], [], [], [], [], [], [], [], [], []]

    for version in version_list:
        for date in time_interval:
            #Using django Q objects to create a dynamic query here
            predicates = [('active', True), ('decommissioned', False), (service, version), ('date', date)]
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
    #percentage = "{0:.1f}".format(num/total_server_count * 100)
    #new_list = [str(version), percentage]
    percentage = 0
    #data[version] = percentage
    return render(request, 'server/stacked_column.htm', {'data': data, 'name': name, 'title': title, 'y_axis_title':y_axis_title, 'version_list':version_list, 'time_interval':time_interval, 'my_array':my_array})



def line_basic(request, string, period, time_range):
    request.GET.get('string')
    request.GET.get('period')
    request.GET.get('time_range')
    data = {}

    name = "Test Name"
    title = "Number Of Active AIX Servers - Last " + time_range + " " + period + "s"

    #for now, we're just going to replace the data as I figure out what I'm doing with this view
    #timestamp = timezone.localtime(now).strftime('%Y-%m-%d')
    #today = datetime.date.today().strftime('%Y-%m-%d')
    #months = ['Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', today]
    #total_server_count = HistoricalAIXData.objects.filter(active=True, decommissioned=False, date=today).count()

    
    months = []
    number_of_servers = []
    number_of_decoms = []
    number_of_prod = []
    number_of_non_prod = []
    interval = 1
    for x in range (0, int(time_range)):
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

        number_of_servers.append(HistoricalAIXData.objects.filter(active=True, decommissioned=False, date=ls).count())
        number_of_decoms.append(HistoricalAIXData.objects.filter(decommissioned=True, date=ls).count())
        number_of_prod.append(HistoricalAIXData.objects.filter(active=True, decommissioned=False, zone_id=2 , date=ls).count())
        number_of_non_prod.append(HistoricalAIXData.objects.filter(active=True, decommissioned=False, zone=1 , date=ls).count())

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
    server = get_object_or_404(AIXServer, pk=aixserver_name)
    frame = get_object_or_404(AIXServer, pk=aixserver_name).frame
    frame_short_name = str(frame)[:3] + '-' + str(frame)[-5:]
    return render(request, 'server/detail.html', {'server': server, 'frame_short_name': frame_short_name})



def linux_server_detail(request, server_linuxserver_id):
    return HttpResponse("Looking at linux server detail for %s." % server_linuxserver_id)

# Create your views here.
