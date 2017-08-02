from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^date', views.date_actuelle, name='index'),
    url(r'^NombreEntites', views.NbEntites, name='NombreEntites'),
    url(r'^UrbanProjectCapacity', views.urban_project_capacity, name='UrbanProjectCapacity'),
    url(r'^Cat_IndustrySector', views.Cat_IndustrySector, name='Cat_IndustrySector'),
    url(r'^Invalid_geom', views.invalid_geom, name='invalid_geom'),
    url(r'^Invalid_proj', views.invalid_proj, name='invalid_proj'),
    url(r'^meshWithoutLandUseArea', views.count_meshWithoutLandUseArea, name='meshWithoutLandUseArea'),
    url(r'^HouseholdWithoutAbstractPerson', views.count_HouseholdWithoutAbstractPerson, name='HouseholdWithoutAbstractPerson'),
]

