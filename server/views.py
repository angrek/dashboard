from __future__ import division #But don't tell anyone, for the sake of the world.
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.http import HttpResponse
from server.models import AIXServer, LinuxServer, Relationships

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template import RequestContext, Context

import json
from django.http import JsonResponse
     
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
