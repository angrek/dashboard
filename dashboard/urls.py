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

    url(r'^admin/', include(admin.site.urls)),
    url(r'^/admin/', include(admin.site.urls)),

    url(r'^server/', include('server.urls')),

    url(r'^todo/', include('todo.urls')),

    url(r'^favicon\.ico$', RedirectView.as_view(url=settings.MEDIA_URL + 'images/favicon.ico')),

    url(r'^$', hello),

    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'), 

)

admin.site.site_header = 'Lizardfish - The Unix Information Dashboard'
admin.site.site_title = 'Lizardfish - The Unix Information Dashboard'
admin.site.index_title = 'Lizardfish - The Unix Information Dashboard'
