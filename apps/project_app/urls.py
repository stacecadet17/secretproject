from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^success$', views.success),
    url(r'^login$', views.login),
    url(r'^wish/create$', views.create),
    url(r'^wish/(?P<id>\d+)$', views.item),
    url(r'^add/(?P<id>\d+)$', views.add),
    url(r'^new$', views.new),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^remove$', views.remove),
    url(r'^logout$', views.logout),
]
