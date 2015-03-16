
from django.conf.urls import patterns, url

from timetracker import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^entry/$', views.entry, name='entry'),

)
