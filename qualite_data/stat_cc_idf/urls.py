from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^date', views.date_actuelle, name='index'),
    url(r'^Accueil', views.accueil, name='index'),
    url(r'^UpdData1', views.launch_UpdData1, name='UpdData'),
    url(r'^UpdData2', views.launch_UpdData2, name='UpdData'),
    url(r'^NombreEntites', views.NbEntites, name='NombreEntites'),
    url(r'^UrbanProjectCapacity', views.urban_project_capacity, name='UrbanProjectCapacity'),
    url(r'^Cat_IndustrySector', views.Cat_IndustrySector, name='Cat_IndustrySector'),
    url(r'^Invalid_geom', views.invalid_geom, name='invalid_geom'),
    url(r'^Invalid_proj', views.invalid_proj, name='invalid_proj'),
    url(r'^contraintesIntegrite', views.count_contraintesIntegrite, name='contraintesIntegrite'),
]

