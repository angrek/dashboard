
from __future__ import division #But don't tell anyone, for the sake of the world.
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.http import HttpResponse
from timetracker.models import Category, Entry
from django.contrib.admin.models import LogEntry

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template import RequestContext, Context

import datetime, calendar
import sys

from django.db.models import Q
import operator

def index(request):
    return render(request, 'timetracker/index.html')

def entry(request):
    entries = Entry.objects.order_by('date')
    context = {'entries': entries}
    return render(request, 'timetracker/entry.html', context)

