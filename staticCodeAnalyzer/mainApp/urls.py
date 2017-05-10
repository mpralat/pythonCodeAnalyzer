from django.conf.urls import url
import datetime
from . import views

urlpatterns = [
    url(r'^add_project/$', views.add_project, name='add_project'),
    url(r'^(?P<project_id>[0-9]+)/$', views.display_project, name='display_project'),
    url(r'^$', views.index, name='index')
]
