from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^create_job$', views.createJob),
    url(r'^add_job/(?P<id>\d+)$', views.addJob),
    url(r'^view/(?P<num>\d+)$', views.viewJob),
    url(r'^back$', views.backtoDashboard),
    url(r'^edit/(?P<id>\d+)$', views.editJob),
    url(r'^cancel/(?P<id>\d+)$', views.deleteFromList),
    url(r'^done/(?P<id>\d+)$', views.deleteFromMyList),
    url(r'^back$', views.backtoDashboard),
]