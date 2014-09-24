from django.conf.urls import patterns, url
from kurama import views

urlpatterns = patterns('',
            url(r'^$', views.index, name='index'),
            url(r'^(?P<taskList_id>\w+)/$', views.detail, name='detail'),
            )
