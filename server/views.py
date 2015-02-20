#UNIX Dashboard views.py

from __future__ import division #But don't tell anyone, for the sake of the world.
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.http import HttpResponse
from server.models import AIXServer, LinuxServer, Relationships, HistoricalAIXData

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template import RequestContext, Context

import datetime, calendar
import sys
     
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

def pie_3d(request, string):
    request.GET.get('string')
    data = {}
    version_list = AIXServer.objects.filter(active=True, exception=False, decommissioned=False).values_list(string , flat=True).distinct()
    version_list = list(set(version_list))
    total_server_count = AIXServer.objects.filter(active=True, exception=False, decommissioned=False).count()
    for version in (version_list):
        if string == 'aix_ssh':
            num = AIXServer.objects.filter(active=True, exception=False, decommissioned=False, aix_ssh=version).count()
            title = "Current distribution of AIX SSH on " + str(total_server_count) + " AIX servers"
        elif string == 'cent_ssh':
            num = AIXServer.objects.filter(active=True, exception=False, decommissioned=False, cent_ssh=version).count()
            title = "Current distribution of Centrify SSH on " + str(total_server_count) + " AIX servers"
        elif string == 'os_level':
            num = AIXServer.objects.filter(active=True, exception=False, decommissioned=False, os_level=version).count()
            title = "Current distribution of OS Level on " + str(total_server_count) + " AIX servers"
        elif string == 'centrify':
            num = AIXServer.objects.filter(active=True, exception=False, decommissioned=False, centrify=version).count()
            title = "Current distribution of Centrify on " + str(total_server_count) + " AIX servers"
        elif string == 'xcelys':
            num = AIXServer.objects.filter(active=True, exception=False, decommissioned=False, xcelys=version).count()
            title = "Current distribution of Xcelys on " + str(total_server_count) + " AIX servers"
        elif string == 'bash':
            num = AIXServer.objects.filter(active=True, exception=False, decommissioned=False, bash=version).count()
            title = "Current distribution of Bash on " + str(total_server_count) + " AIX servers"
        elif string == 'ssl':
            num = AIXServer.objects.filter(active=True, exception=False, decommissioned=False, ssl=version).count()
            title = "Current distribution of SSL on " + str(total_server_count) + " AIX servers"
        elif string == 'imperva':
            num = AIXServer.objects.filter(active=True, exception=False, decommissioned=False, imperva=version).count()
            title = "Current distribution of Imperva on " + str(total_server_count) + " AIX servers"
        elif string == 'netbackup':
            num = AIXServer.objects.filter(active=True, exception=False, decommissioned=False, netbackup=version).count()
            title = "Current distribution of Netbackup on " + str(total_server_count) + " AIX servers"
        percentage = "{0:.1f}".format(num/total_server_count * 100)
        new_list = [str(version), percentage]
        data[version] = percentage

    name = "Percentage"
    return render(request, 'server/pie_3d.htm', {'data': data, 'name': name, 'title': title})


def stacked_column(request, os, zone, service, period, time_range):
    request.GET.get('os')
    request.GET.get('zone')
    request.GET.get('service')
    request.GET.get('period')
    request.GET.get('time_range')
    data = {}

    os = os.upper()
    title = "Historical distribution of " + service + " on " + os + " servers by " + period

    #today = datetime.date.today().strftime('%Y-%m-%d')

    #time_interval is the list of dates to gather data from, whether by day, week, month 
    time_interval = []
    #number_of_servers = []

    #interval is the offset for timedelta to get last sunday every week, every month or whatever
    interval = 1

    #Here we're going to get all of the versions of whatever software exist in a given date range.
    #last_date is the newest date of the range on the right of the graph
    if period == 'week':
        last_date = (datetime.date.today() - datetime.timedelta(days = (datetime.date.today().weekday() + interval))).strftime('%Y-%m-%d')
        offset = (int(time_range) * 7) +1
    elif period == 'day':
        last_date = datetime.date.today().strftime('%Y-%m-%d')
        offset = int(time_range) + 1
    elif period == 'month':
        #ok, so month goes by end of month? for now until told differently, this month will go by todays date
        last_date = datetime.date.today().strftime('%Y-%m-%d')
        offset = (int(time_range) * 30) +1
    else:
        #Uh, 404?
        sys.exit()
        
    first_date = (datetime.date.today() - datetime.timedelta(days = (datetime.date.today().weekday() + offset))).strftime('%Y-%m-%d')

    if service == 'os_level':
        if zone == 'all':
            version_list = HistoricalAIXData.objects.filter(active=True, decommissioned=False, date__range=[first_date, last_date]).exclude(name__name__contains='vio').exclude(os_level='None').values_list(service , flat=True).distinct()
        elif zone == 'Production':
            version_list = HistoricalAIXData.objects.filter(active=True, decommissioned=False, zone='Production', date__range=[first_date, last_date]).exclude(name__name__contains='vio').exclude(os_level='None').values_list(service , flat=True).distinct()
        elif zone == 'nonproduction':
            version_list = HistoricalAIXData.objects.filter(active=True, decommissioned=False, zone='Production', date__range=[first_date, last_date]).exclude(name__name__contains='vio').exclude(os_level='None').values_list(service , flat=True).distinct()
        else:
            sys.exit()
    else:
        version_list = HistoricalAIXData.objects.filter(active=True, decommissioned=False, date__range=[first_date, last_date]).values_list(service , flat=True).distinct()
    version_list = list(set(version_list))


    #Populate time_interval with the dates for the labels and queries
    for x in range (0, (int(time_range))):
        #FIXME For some reason my 'day' last date is two days before today.... so this is hackish for now at best
        if period == 'day':
            test = 1
        else:
            test = 0
        last_date = (datetime.date.today() - datetime.timedelta(days = (datetime.date.today().weekday() + interval ))).strftime('%Y-%m-%d')
        if x == 0 and period=='day':
            last_date = datetime.date.today()
        
        time_interval.append(last_date)
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


    #number_of_servers.append(HistoricalAIXData.objects.filter(active=True, decommissioned=False, date=last_date).count())
    #Ok, this is a bit different, we're going to have to iterate over the date and push the number of servers into a list across dates
    version_counter = 0
    date_counter = 0
    my_array = [[], [], [], [], [], [], [], [], [], [], [], [], [], []]
    #myarray = [[], [], [], [], [], []. [], [], [], [], [], [], [], []]
    #my_array = []
    for version in version_list:
        #FIXME - this os_level check needs to go somewhere else, but it's fine here for testing I guess, but it's needed more above
        for date in time_interval:
            if service == 'os_level':
                num = HistoricalAIXData.objects.filter(active=True, decommissioned=False, os_level=version, date=date).count()
            elif service == 'aix_ssh':
                num = HistoricalAIXData.objects.filter(active=True, decommissioned=False, aix_ssh=version, date=date).count()
            elif service == 'cent_ssh':
                num = HistoricalAIXData.objects.filter(active=True, decommissioned=False, cent_ssh=version, date=date).count()
            elif service == 'centrify':
                num = HistoricalAIXData.objects.filter(active=True, decommissioned=False, centrify=version, date=date).count()
            elif service == 'xcelys':
                num = HistoricalAIXData.objects.filter(active=True, decommissioned=False, xcelys=version, date=date).count()
            elif service == 'imperva':
                num = HistoricalAIXData.objects.filter(active=True, decommissioned=False, imperva=version, date=date).count()
            elif service == 'netbackup':
                num = HistoricalAIXData.objects.filter(active=True, decommissioned=False, netbackup=version, date=date).count()
            elif service == 'bash':
                num = HistoricalAIXData.objects.filter(active=True, decommissioned=False, bash=version, date=date).count()
            elif service == 'ssl':
                num = HistoricalAIXData.objects.filter(active=True, decommissioned=False, ssl=version, date=date).count()

    #        num = 1
            if date_counter == 0:
                my_array[version_counter] = [num]
    #            my_array[1][1] = [num]
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
