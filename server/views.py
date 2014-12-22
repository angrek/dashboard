from django.http import Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.http import HttpResponse
from server.models import AIXServer, LinuxServer

def index(request):
    first_ten_servers = AIXServer.objects.order_by('name')[:10]
    context = {'first_ten_servers': first_ten_servers}
    return render(request, 'server/index.html', context)

def stacks(request):
    red_servers = AIXServer.objects.filter(stack__name = 'Red').order_by('name')
    yellow_servers = AIXServer.objects.filter(stack__name = 'Yellow').order_by('name')
    green_servers = AIXServer.objects.filter(stack__name = 'Green').order_by('name')
    orange_servers = AIXServer.objects.filter(stack__name = 'Orange').order_by('name')
    #server_list = AIXServer.objects.filter(stack__name ='Red')
    context = {'red_servers' : red_servers,
        'yellow_servers': yellow_servers,
        'green_servers': green_servers,
        'orange_servers': orange_servers}
    return render(request, 'server/stacks.html', context)


def detail(request, aixserver_name):
    #try:
    #    server = AIXServer.objects.get(pk=aixserver_name)
    #except:
    #    raise Http404
    server = get_object_or_404(AIXServer, pk=aixserver_name)
    return render(request, 'server/detail.html', {'server': server})



def linux_server_detail(request, server_linuxserver_id):
    return HttpResponse("Looking at linux server detail for %s." % server_linuxserver_id)

# Create your views here.
