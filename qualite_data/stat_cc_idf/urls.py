from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^date', views.date_actuelle, name='index'),
    url(r'^Accueil', views.accueil, name='accueil'),
    url(r'^UpdData1', views.launch_UpdData1, name='UpdData'),
    url(r'^UpdData2', views.launch_UpdData2, name='UpdData'),
    url(r'^UpdData3', views.launch_UpdData3, name='UpdData'),
    url(r'^UpdData4', views.launch_UpdData4, name='UpdData'),
    url(r'^UpdData5', views.launch_UpdData5, name='UpdData'),
    url(r'^UpdData6', views.launch_UpdData6, name='UpdData'),
    url(r'^UpdData7', views.launch_UpdData7, name='UpdData'),
    url(r'^UpdData8', views.launch_UpdData8, name='UpdData'),
    url(r'^UpdData', views.launch_UpdAllData, name='UpdData'),
    url(r'^NombreEntites', views.NbEntites, name='NombreEntites'),
    url(r'^UrbanProjectCapacity', views.urban_project_capacity, name='UrbanProjectCapacity'),
    url(r'^Cat_IndustrySector', views.Cat_IndustrySector, name='Cat_IndustrySector'),
    url(r'^Invalid_geom', views.invalid_geom, name='invalid_geom'),
    url(r'^Invalid_proj', views.invalid_proj, name='invalid_proj'),
    url(r'^contraintesIntegrite', views.count_contraintesIntegrite, name='contraintesIntegrite'),
    url(r'^cartoCC', views.cartoCC, name='cartoCC'),
    url(r'^countStat', views.count_stat, name='countStat'),
]

