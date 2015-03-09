# UNIX Dashboard urls.py

from django.conf.urls import patterns, url

from server import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^jquerytest/$', views.jquerytest, name='jquerytest'),
    url(r'^stacks/$', views.stacks, name='stacks'),
    url(r'^frames/$', views.frames, name='frames'),
    url(r'^wpars/$', views.wpars, name='wpars'),
    #url(r'^pie_ssh/$', views.pie_ssh, name='pie_ssh'),
    #url(r'^3d_pie/aix_ssh|cent_ssh/$', views.pie_ssh, name='pie_ssh'),
    url(r'^pie_3d/(?P<os>(.*)+)/(?P<zone>(.*)+)/(?P<service>(.*)+)$', views.pie_3d, name='pie_3d'),
    url(r'^stacked_column/(?P<os>(.*)+)/(?P<zone>(.*)+)/(?P<service>(.*)+)/(?P<period>(.*)+)/(?P<time_range>(.*)+)$', views.stacked_column, name='stacked_column'),
    url(r'^line_basic/(?P<string>(.*)+)/(?P<period>(.*)+)/(?P<time_range>(.*)+)$', views.line_basic, name='line_basic'),

    #Can I do something like this? This is what I need....
    #url(r'^3d_pie/<historical_today>/<service>/$', views.pie_ssh, name='pie_ssh'),

    url(r'^(?P<aixserver_name>(.*)+)/$', views.detail, name='detail'),


)
