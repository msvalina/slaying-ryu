from django.conf.urls import patterns, url
from kurama import views

urlpatterns = patterns('',
            url(r'^$', views.index, name='index'),
            url(r'^(?P<task_id>\w+)/$', views.detail, name='detail'),
            url(r'^(?P<task_list>\d+-\w+&\w+)/$', views.task_list, name='task_list'),
            url(r'^tag/(?P<tag>#\w+#|\$\w+\$|\*\w+\*|=|"\w+")/$', views.tag, name='tag'),
            url(r'^tagname/(?P<tagname>[\w\ ]+)/$', views.tagname, name='tagname'),
            url(r'^stats$', views.stats, name='stats'),
            url(r'^about$', views.about, name='about'),
            url(r'^current_week$', views.current_week, name='current_week'),
            url(r'^last_week$', views.last_week, name='last_week'),
            url(r'^last_month$', views.last_month, name='last_month'),
            url(r'^last_quarter$', views.last_quarter, name='last_quarter'),
            url(r'^last_year$', views.last_year, name='last_year'),
            url(r'^populate$', views.populate, name='populate'),
            url(r'^graph$', views.graph, name='graph'),
            )
