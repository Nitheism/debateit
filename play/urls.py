from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^debate', views.room, name='debate'),
]
