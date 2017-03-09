from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^profile/(?P<username>[a-zA-Z0-9]+)$', views.profile, name='profile'),
    url(r'^edit_profile', views.profile_edit, name='edit_profile'),
    url(r'^ranklist', views.ranklist, name='ranklist'),
    url(r'^report', views.report_form, name='report'),

]
