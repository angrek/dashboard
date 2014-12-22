from django.conf.urls import patterns, url

from server import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    url(r'^(?P<aixserver_name>(.*)+)/$', views.detail, name='detail'),


)
