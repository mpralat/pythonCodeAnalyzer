from django.conf.urls import url
import datetime
from . import views

urlpatterns = [
    url(r'^add_project/$', views.add_project, name='add_project'),
    url(r'^clone_project/$', views.clone_project, name='clone_project'),
    url(r'^generate_report/$', views.generate_report, name='generate_report'),
    url(r'^project/(?P<project_id>[0-9]+)/$', views.display_project, name='display_project'),
    url(r'^report/(?P<report_id>[0-9]+)/$', views.display_report, name='display_report'),
    url(r'^$', views.index, name='index')
]
