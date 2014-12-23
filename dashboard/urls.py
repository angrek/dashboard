from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
from dashboard.views import hello

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dashboard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^server/', include('server.urls')),

    url(r'^todo/', include('todo.urls')),

    url(r'^favicon\.ico$', RedirectView.as_view(url=settings.MEDIA_URL + 'images/favicon.ico')),

    url(r'^$', hello),

    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'), 

)

#if settings.DEBUG:
#    urlpatterns += patterns(
#            'django.view.static',
#            (r'media/(?P<path>.*)',
#            'serve',
#            {'document_root': settings.MEDIA_ROOT}),)
