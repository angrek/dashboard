
from __future__ import division #But don't tell anyone, for the sake of the world.
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from timetracker.models import Category, Entry
from timetracker.forms import PostForm


from django.contrib.admin.models import LogEntry

from django.contrib.auth.decorators import login_required, user_passes_test
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
            if description and notes and hours:
                new_category = Category.objects.get(name=request.POST['category' + str(x)])

                entry = Entry.objects.create(description=description, category=new_category, username=username, hours=hours, notes=notes)
        entries = Entry.objects.filter(username=username).order_by('date')
        return HttpResponseRedirect('show_entries/0000-00-00', {'entries': entries})

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
        form = PostForm()
    else:
        #FIXME THIS IS THE ONE BEING USED, DUH
        form = PostForm(request.POST) #BIND data from request.POST into a PostForm

        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        date_list = Entry.objects.filter(username=request.user, date__range=[start_date, end_date]).values_list('date', flat=True).distinct()

        a = Category.objects.get(short_name='A')
        i = Category.objects.get(short_name='I')
        o = Category.objects.get(short_name='O')
        p = Category.objects.get(short_name='P')

        date_dict = {}
        date_totals = {}
        temp_totals = {}
        for date in date_list:
            entry = Entry.objects.filter(username=request.user, date=date)
            date_dict[date] = entry

            #we need the total hours for each category for the date
            total_a = 0
            total_i = 0
            total_o = 0
            total_p = 0
            for x in entry:
                hours = x.hours
                if x.category == a:
                    total_a += hours
                elif x.category == i:
                    total_i += hours
                elif x.category == o:
                    total_o += hours
                elif x.category == p:
                    total_i += hours
            temp_totals = {'A': str(total_a), 'I': str(total_i), 'O': str(total_o), 'P': str(total_p)}
            date_totals[date] = temp_totals

        context = {'start_date':start_date, 'end_date':end_date, 'date_dict':date_dict, 'total_a':total_a, 'date_totals': date_totals, 'date_list': date_list}
        return render(request, 'timetracker/view_report.html', context)

    #these don't reallyl need to be here, we'll never hit the page otherwise...
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
@user_passes_test(lambda u: u.groups.filter(name='timetracker_manager').count() == 1, login_url='/timetracker/denied/')
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

@login_required
@user_passes_test(lambda u: u.groups.filter(name='timetracker_manager').count() == 1, login_url='/timetracker/denied/')
def daily_manager_report(request, date):
    temp_list = User.objects.all()
    group_list = []

    #FIXME if multiple groups use this we'll need to grab the manager's group and use that
    #get all the users in the correct group
    for user in temp_list:
        if user.groups.filter(name='unix').exists():
            group_list.append(user)

    request.GET.get('date')
    if date == '0000-00-00':
        date = datetime.date.today()
    else:
        date = datetime.date(int(date[:4]), int(date[5:7]), int(date[-2:]))

    #get dates for the bread crumbs
    previous = (date - timedelta(days = 1)).strftime('%Y-%m-%d')
    next = (date + timedelta(days = 1)).strftime('%Y-%m-%d')
  
    entries = {}
    total_hours_by_user = {}
    total_hours = {}
    tmp_totals = {}
    users_with_entries = []
    users_with_no_entries = []

    a = Category.objects.get(short_name='A')
    i = Category.objects.get(short_name='I')
    o = Category.objects.get(short_name='O')
    p = Category.objects.get(short_name='P')

    overall_total_a = 0
    overall_total_i = 0
    overall_total_o = 0
    overall_total_p = 0

    for name in group_list: 
        tmp_total_hours = 0
        total_a = 0
        total_i = 0
        total_o = 0
        total_p = 0

        if Entry.objects.filter(username=name, date=date):
            users_entries = Entry.objects.filter(username=name, date=date)
            for entry in users_entries:
                hours = entry.hours
                tmp_total_hours += hours
                if entry.category == a:
                    total_a += hours
                if entry.category == i:
                    total_i += hours
                if entry.category == o:
                    total_o += hours
                if entry.category == p:
                    total_p += hours

            overall_total_a += total_a
            overall_total_i += total_i
            overall_total_o += total_o
            overall_total_p += total_p

            temp_totals = {'A': str(total_a), 'I': str(total_i), 'O':str(total_o), 'P':str(total_p)}
            total_hours_by_user[name] = temp_totals

            users_with_entries.append(str(name.username))
            entries[name] = users_entries

        else:
            users_with_no_entries.append(str(name.username))

    total_hours = {'A': str(overall_total_a), 'I': str(overall_total_i), 'O':str(overall_total_o), 'P':str(overall_total_p)}

    #Now we need to get the totals


    #totals = {}
    #for tmp_name in users_with_entries:
    #    temp_total = 0
    #    x = entries[tmp_name]
    #    for y in x:
    #       temp_total += y.hours 


    context = {'entries': entries, 'previous':previous, 'next':next, 'total_hours_by_user':total_hours_by_user, 'total_hours': total_hours, 'date':date, 'users_with_no_entries':users_with_no_entries}
    return render(request, 'timetracker/daily_manager_report.html', context)

            
