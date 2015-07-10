from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
from dashboard.views import hello
from django.contrib.admin.sites import AdminSite

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dashboard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^/images/favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin', include(admin.site.urls)),

    #I HATE that I have to do this, but...
    url(r'^server/', include('server.urls')),
    url(r'^server', include('server.urls')),
    url(r'^timetracker/', include('timetracker.urls')),
    url(r'^timetracker', include('timetracker.urls')),
    url(r'^todo/', include('todo.urls')),
    url(r'^todo', include('todo.urls')),


    url(r'^$', hello),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'), 

)

admin.site.site_header = 'Lizardfish - The Unix Information Dashboard'
admin.site.site_title = 'Lizardfish - The Unix Information Dashboard'
admin.site.index_title = 'Lizardfish - The Unix Information Dashboard'
