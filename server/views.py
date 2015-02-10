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

import datetime
     
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


def stacked_column(request, string):
    request.GET.get('string')
    data = {}
    total_server_count = AIXServer.objects.filter(active=True, exception=False, decommissioned=False).count()
     
    name = "Test Name"
    title = "Number Of AIX Servers"
    return render(request, 'server/stacked_column.htm', {'data': data, 'name': name, 'title': title})

def line_basic(request, string, string2):
    request.GET.get('string')
    request.GET.get('string2')
    data = {}
    #rather than /aix/week we could change this and make it something like /total_servers/all /total_servers/linux
    #we could branch this out as well like /aix_versions/linux

    #Not filtering exceptions as they are active servers and we need a total count
    total_server_count = HistoricalAIXData.objects.filter(active=True, decommissioned=False, date='2015-02-09').count()
    name = "Test Name"
    title = "Number Of Active AIX Servers - Last 12 weeks"
    months = ['Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb']

    #for now, we're just going to replace the data as I figure out what I'm doing with this view
    if string2 == 'week':
        #timestamp = timezone.localtime(now).strftime('%Y-%m-%d')
        today = datetime.date.today().strftime('%Y-%m-%d')
        #months = ['Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', today]
        total_server_count = HistoricalAIXData.objects.filter(active=True, decommissioned=False, date=today).count()

        
        months = []
        number_of_servers = []
        number_of_decoms = []
        number_of_prod = []
        number_of_non_prod = []
        interval = 1
        for x in range (0, 12):
            ls = datetime.date.today() - datetime.timedelta(days = (datetime.date.today().weekday() + interval))
            ls = ls.strftime('%Y-%m-%d')
            months.append(ls)
            interval = interval + 7

            count = HistoricalAIXData.objects.filter(active=True, decommissioned=False, date=ls).count()
            number_of_servers.append(count)

            decom_count = HistoricalAIXData.objects.filter(decommissioned=True, date=ls).count()
            number_of_decoms.append(decom_count)

            prod_count = HistoricalAIXData.objects.filter(active=True, decommissioned=False, zone_id=2 , date=ls).count()
            number_of_prod.append(prod_count)

            non_prod_count = HistoricalAIXData.objects.filter(active=True, decommissioned=False, zone=1 , date=ls).count()
            number_of_non_prod.append(non_prod_count)


        months.reverse()
        number_of_servers.reverse()
        number_of_decoms.reverse() 
        number_of_prod.reverse()
        number_of_non_prod.reverse()

    return render(request, 'server/line_basic.htm', {'data': data, 'months': months, 'number_of_servers': number_of_servers, 'number_of_decoms': number_of_decoms, 'number_of_prod': number_of_prod, 'number_of_non_prod': number_of_non_prod, 'name': name, 'title': title, 'total_server_count': total_server_count})



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
