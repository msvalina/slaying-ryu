from django.conf.urls import patterns, url
from kurama import views

urlpatterns = patterns('',
            url(r'^$', views.index, name='index'),
            url(r'^(?P<task_id>\w+)/$', views.detail, name='detail'),
            url(r'^(?P<task_list>\d+-\w+&\w+)/$', views.task_list, name='task_list'),
            url(r'^tag/(?P<tag>#\w+#|\$\w+\$|\*\w+\*|=|"\w+")/$', views.tag, name='tag'),
            url(r'^tagname/(?P<tagname>[\w\ ]+)/$', views.tagname, name='tagname'),
            url(r'^stats/timerange=(?P<time_range>\w+)/$', views.stats, name='stats'),
            url(r'^stats/timerange=(?P<time_range>\w+)/tl=(?P<tl>\w+)/$', views.stats, name='stats'),
            url(r'^stats/timerange=(?P<time_range>\w+)/tl=(?P<tl>\w+)/tag=(?P<tag>\w+)/$', views.stats, name='stats'),
            url(r'^stats$', views.stats, name='stats'),
            url(r'^about$', views.about, name='about'),
            url(r'^current_week$', views.current_week, name='current_week'),
            url(r'^populate$', views.populate, name='populate'),
            url(r'^graph$', views.graph, name='graph'),
            )
