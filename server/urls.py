from django.conf.urls import patterns, url

from server import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^stacks/$', views.stacks, name='stacks'),
    url(r'^wpars/$', views.wpars, name='wpars'),
    #url(r'^pie_ssh/$', views.pie_ssh, name='pie_ssh'),
    #url(r'^3d_pie/aix_ssh|cent_ssh/$', views.pie_ssh, name='pie_ssh'),
    url(r'^pie_3d/(?P<string>(.*)+)/$', views.pie_3d, name='pie_3d'),
    url(r'^stacked_column/(?P<string>(.*)+)/$', views.stacked_column, name='stacked_column'),
    url(r'^line_basic/(?P<string>(.*)+)/$', views.line_basic, name='line_basic'),

    #Can I do something like this? This is what I need....
    #url(r'^3d_pie/<historical_today>/<service>/$', views.pie_ssh, name='pie_ssh'),

    url(r'^(?P<aixserver_name>(.*)+)/$', views.detail, name='detail'),


)
