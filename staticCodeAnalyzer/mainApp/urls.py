from django.conf.urls import url
import datetime
from . import views

urlpatterns = [
    url(r'/', views.index,  name='index'),
]
