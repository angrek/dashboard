from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dashboard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^server/', include(admin.site.urls)),
    #url(r'^todo/', include(admin.site.urls)),
    url(r'^todo/', include('todo.urls')),
    url(r'^favicon\.ico$', RedirectView.as_view(url=settings.MEDIA_URL + 'images/favicon.ico')),
)

#if settings.DEBUG:
#    urlpatterns += patterns(
#            'django.view.static',
#            (r'media/(?P<path>.*)',
#            'serve',
#            {'document_root': settings.MEDIA_ROOT}),)
