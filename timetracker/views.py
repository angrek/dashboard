
from __future__ import division #But don't tell anyone, for the sake of the world.
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from timetracker.models import Category, Entry
from timetracker.forms import PostForm


from django.contrib.admin.models import LogEntry

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template import RequestContext, Context
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

import datetime, calendar
import sys

from django.db.models import Q
import operator

@login_required
def index(request):
    return render(request, 'timetracker/index.html')

@login_required
def add_entry(request):
    if request.method == 'GET':
        form = PostForm()
    else:
        #A POST request: Handle form upload
        form = PostForm(request.POST) #BIND data from request.POST into a PostForm

        #if data is valid, create a new post and redirect the user
        #if form.is_valid():
        #description = form.cleaned_data['description']
        #category = form.cleaned_data['category']
        #hours = form.cleaned_data['hours']
        #notes = form.cleaned_data['notes']
        description = request.POST['description']
        hours = request.POST['hours']
        notes = request.POST['notes']
        username = User.objects.get(username=request.user)
        new_category = Category.objects.get(name=request.POST['category'])

        entry = Entry.objects.create(description=description, category=new_category, username=username, hours=hours, notes=notes)
        entries = Entry.objects.filter(username=username).order_by('date')
        return HttpResponseRedirect('show_entries', {'entries': entries})

    return render(request, 'timetracker/add_entry.html', {
        'form': form,
    })

@login_required
def add_report(request):
    if request.method == 'GET':
        form = PostForm()
    else:
        #A POST request: Handle form upload
        form = PostForm(request.POST) #BIND data from request.POST into a PostForm

        #if data is valid, create a new post and redirect the user
        if form.is_valid():
            name = form.cleaned_data['name']
            short_name = form.cleaned_data['short_name']
            description = form.cleaned_data['description']
            category = Category.objects.create(name=name, short_name=short_name, description=description)
            categories = Category.objects.order_by('name')
            return HttpResponseRedirect('show_categories', {'categories': categories})

    return render(request, 'timetracker/add_category.html', {
        'form': form,
    })

@login_required
def show_reports(request):
    entries = Entry.objects.order_by('date')
    context = {'entries': entries}
    return render(request, 'timetracker/report.html', context)

@login_required
def show_categories(request):
    categories = Category.objects.order_by('name')
    context = {'categories': categories}
    return render(request, 'timetracker/show_categories.html', context)

@login_required
def show_entries(request):
    entries = Entry.objects.order_by('date')
    context = {'entries': entries}
    return render(request, 'timetracker/show_entries.html', context)


@login_required
def add_category(request):
    if request.method == 'GET':
        form = PostForm()
    else:
        #A POST request: Handle form upload
        form = PostForm(request.POST) #BIND data from request.POST into a PostForm

        #if data is valid, create a new post and redirect the user
        if form.is_valid():
            name = form.cleaned_data['name']
            short_name = form.cleaned_data['short_name']
            description = form.cleaned_data['description']
            category = Category.objects.create(name=name, short_name=short_name, description=description)
            categories = Category.objects.order_by('name')
            return HttpResponseRedirect('show_categories', {'categories': categories})

    return render(request, 'timetracker/add_category.html', {
        'form': form,
    })

            
