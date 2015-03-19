
from django.conf.urls import patterns, url

from timetracker import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^add_category$', 'timetracker.views.add_category', name='add_category'),
    url(r'^add_entry$', 'timetracker.views.add_entry', name='add_entry'),
    url(r'^add_report$', 'timetracker.views.add_report', name='add_report'),
    url(r'^show_categories/$', views.show_categories, name='show_categories'),
    url(r'^show_entries/$', views.show_entries, name='show_entries'),
    url(r'^show_reports/$', views.show_reports, name='show_reports'),

)
