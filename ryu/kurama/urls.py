from django.conf.urls import patterns, url
from kurama import views

urlpatterns = patterns('',
            url(r'^$', views.index, name='index'),
            url(r'^(?P<task_id>\w+)/$', views.detail, name='detail'),
            url(r'^(?P<task_list>\d+-\w+&\w+)/$', views.task_list, name='task_list'),
            url(r'^stats$', views.stats, name='stats'),
            url(r'^current_week$', views.current_week, name='current_week'),
            url(r'^last_week$', views.last_week, name='last_week'),
            url(r'^last_month$', views.last_month, name='last_month'),
            url(r'^last_quarter$', views.last_quarter, name='last_quarter'),
            url(r'^last_year$', views.last_year, name='last_year'),
            url(r'^populate$', views.populate, name='populate'),
            )
