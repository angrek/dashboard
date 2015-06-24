# UNIX Dashboard urls.py

from django.conf.urls import patterns, url

from server import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^jquerytest/$', views.jquerytest, name='jquerytest'),
    url(r'^stacks/(?P<os>(.*)+)/(?P<zone>(.*)+)$', views.stacks, name='stacks'),
    url(r'^stacks/(?P<os>(.*)+)/(?P<zone>(.*)+)/$', views.stacks, name='stacks'),
    url(r'^frames$', views.frames, name='frames'),
    url(r'^frames/$', views.frames, name='frames'),
    url(r'^wpars$', views.wpars, name='wpars'),
    url(r'^wpars/$', views.wpars, name='wpars'),
    url(r'^java$', views.java, name='java'),
    url(r'^java/$', views.java, name='java'),

    url(r'^local_users.txt$', views.local_users, name='local_users'),
    url(r'^local_users.txt/$', views.local_users, name='local_users'),
    #url(r'^pie_ssh/$', views.pie_ssh, name='pie_ssh'),
    #url(r'^3d_pie/aix_ssh|cent_ssh/$', views.pie_ssh, name='pie_ssh'),

    url(r'^pie_3d/(?P<os>(.*)+)/(?P<zone>(.*)+)/(?P<service>(.*)+)$', views.pie_3d, name='pie_3d'),

    url(r'^pie_3d_pools/(?P<frame>(.*)+)/$', views.pie_3d_pools, name='pie_3d_pools'),
    url(r'^pie_3d_pools/(?P<frame>(.*)+)$', views.pie_3d_pools, name='pie_3d_pools'),

    url(r'^stacked_column/(?P<os>(.*)+)/(?P<zone>(.*)+)/(?P<service>(.*)+)/(?P<period>(.*)+)/(?P<time_range>(.*)+)$', views.stacked_column, name='stacked_column'),
    url(r'^line_basic/(?P<string>(.*)+)/(?P<period>(.*)+)/(?P<time_range>(.*)+)$', views.line_basic, name='line_basic'),

    url(r'^treemap/$', views.treemap, name='treemap'),
    url(r'^treemap$', views.treemap, name='treemap'),

    #Can I do something like this? This is what I need....
    #url(r'^3d_pie/<historical_today>/<service>/$', views.pie_ssh, name='pie_ssh'),

    url(r'^(?P<aixserver_name>(.*)+)/$', views.detail, name='detail'),


)
