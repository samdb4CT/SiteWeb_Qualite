from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^date', views.date_actuelle, name='index'),
    url(r'^NombreEntites', views.NbEntites, name='NombreEntites'),
]

