
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
from django.http import Http404

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

import datetime, calendar
from datetime import timedelta
import sys

from django.db.models import Q
import operator

@login_required
def index(request):
    return render(request, 'timetracker/index.html')

@login_required
def add_entry(request):
    categories = Category.objects.all().order_by('name')
    if request.method == 'GET':
        form = PostForm()
    else:
        #A POST request: Handle form upload
        form = PostForm(request.POST) #BIND data from request.POST into a PostForm
        #notes = form.cleaned_data['notes']
        for x in range(1, 6): 
            description = request.POST['description' + str(x)]
            hours = request.POST['hours' + str(x)]
            notes = request.POST['notes' + str(x)]
            username = User.objects.get(username=request.user)
            new_category = Category.objects.get(name=request.POST['category' + str(x)])

            entry = Entry.objects.create(description=description, category=new_category, username=username, hours=hours, notes=notes)
        entries = Entry.objects.filter(username=username).order_by('date')
        return HttpResponseRedirect('show_entries', {'entries': entries})

    return render(request, 'timetracker/add_entry.html', {
        'form': form,
        'categories': categories,
    })

@login_required
def show_entries(request, date):
    request.GET.get('date')
    if date == '0000-00-00':
        date = datetime.date.today()
    else:
        date = datetime.date(int(date[:4]), int(date[5:7]), int(date[-2:]))
    previous = (date - timedelta(days = 1)).strftime('%Y-%m-%d')
    next = (date + timedelta(days = 1)).strftime('%Y-%m-%d')
    entries = Entry.objects.filter(username=request.user, date=date)
    context = {'entries': entries, 'previous':previous, 'next':next, 'date':date}
    return render(request, 'timetracker/show_entries.html', context)

@login_required
def add_report(request):
    if request.method == 'GET':
        form = PostForm()
    else:
        #A POST request: Handle form upload
        form = PostForm(request.POST) #BIND data from request.POST into a PostForm

        #if data is valid, create a new post and redirect the user
        start_date = request.POST.get('start_date', False)
        end_date = request.POST.get('end_date', False)
        entries = Entry.objects.filter(username=request.user).order_by('date')
        context = {'entries':entries, 'start_date': start_date, 'end_date':end_date}
        return render(request, 'timetracker/view_report.html', context)
        #return HttpResponseRedirect('view_report', {'start_date': start_date,'end_date':end_date})
        #return HttpResponseRedirect('view_report', {'start_date': start_date,'end_date':end_date})

    return render(request, 'timetracker/add_report.html', {
        'form': form,
    })

@login_required
def view_report(request):
    if request.method == 'GET':
        #A POST request: Handle form upload
        form = PostForm(request.POST) #BIND data from request.POST into a PostForm

        #if data is valid, create a new post and redirect the user
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        entries = Entry.objects.filter(username=request.user).order_by('date')
        start_date = '2015-03-13'
        context = {'entries': entries, 'start_date':start_date, 'end_date':end_date}
        #FIXME testing one vs the other
        #return HttpResponseRedirect('view_report', {'entries':entries, 'start_date': start_date, 'end_date':end_date})
        return render(request, 'timetracker/view_report.html', context)
        #form = PostForm()
    else:
        #A POST request: Handle form upload
        form = PostForm(request.POST) #BIND data from request.POST into a PostForm

        #if data is valid, create a new post and redirect the user
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        entries = Entry.objects.filter(username=request.user).order_by('date')
        context = {'entries': entries, 'start_date':start_date, 'end_date':end_date}
        #FIXME testing one vs the other
        #return HttpResponseRedirect('view_report', {'start_date': start_date})
        return render(request, 'timetracker/view_report.html', context)
    entries = Entry.objects.order_by('date')
    context = {'entries': entries}
    return render(request, 'timetracker/show_reports.html', context)

@login_required
def show_reports(request):
    entries = Entry.objects.order_by('date')
    context = {'entries': entries}
    return render(request, 'timetracker/show_reports.html', context)

@login_required
def show_categories(request):
    user = request.user
    if not user.groups.filter(name='category_admin').exists():
        raise Http404    
    categories = Category.objects.order_by('name')
    context = {'categories': categories}
    return render(request, 'timetracker/show_categories.html', context)


@login_required
def add_category(request):
    user = request.user
    if not user.groups.filter(name='category_admin').exists():
        raise Http404    
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

            
