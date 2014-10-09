from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'kurama.views.index', name='ryu'),
    url(r'^kurama/', include('kurama.urls', namespace="kurama")),
    url(r'^admin/', include(admin.site.urls)),
)
