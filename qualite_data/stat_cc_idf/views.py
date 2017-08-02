#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import Http404
from datetime import datetime
import django_tables2 as tables
from django_tables2 import RequestConfig
from stat_cc_idf.models import VerifNombreEntites
from stat_cc_idf.models import VerifUrbanProjectCapacity
from stat_cc_idf.models import VerifTypeInductrySector
from stat_cc_idf.models import VerifInvalidGeometry
from stat_cc_idf.models import VerifProjection
from stat_cc_idf.models import VerifFieldMesh
from stat_cc_idf.models import VerifHousehold

def date_actuelle(request):
    return render(request, 'date.html', {'date': datetime.now()})
    
def NbEntites(request):
    nbEntites = VerifNombreEntites.objects.all()
    table = EntiteTable(VerifNombreEntites.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=500)
    RequestConfig(request,paginate={'per_page': 500}).configure(table)
    return render(request,'stat_NombreEntites.html',{'nb_ent':table})
    

class EntiteTable(tables.Table):
    class Meta:
        model = VerifNombreEntites
        attrs = {'class': 'palegreen'}
        
def urban_project_capacity(request):
    upc = VerifUrbanProjectCapacity.objects.all()
    table = UPCTable(VerifUrbanProjectCapacity.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=500)
    RequestConfig(request,paginate={'per_page': 500}).configure(table)
    return render(request,'UrbanProjectCapacity.html',{'urban_project_capacity':table})
# Create your views here.

class UPCTable(tables.Table):
    class Meta:
        model = VerifUrbanProjectCapacity
        attrs = {'class': 'green'}
        
def Cat_IndustrySector(request):
    upc = VerifTypeInductrySector.objects.all()
    table = Ind_sectorTable(VerifTypeInductrySector.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=500)
    RequestConfig(request,paginate={'per_page': 500}).configure(table)
    return render(request,'categories_IndustrySector.html',{'cat_indSector':table})
# Create your views here.

class Ind_sectorTable(tables.Table):
    class Meta:
        model = VerifTypeInductrySector
        attrs = {'class': 'green'}
        
def invalid_geom (request):
    upc = VerifInvalidGeometry.objects.all()
    table = invalid_geomTable(VerifInvalidGeometry.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=500)
    RequestConfig(request,paginate={'per_page': 500}).configure(table)
    return render(request,'verif_invalid_geom.html',{'inv_geom':table})
# Create your views here.

class invalid_geomTable(tables.Table):
    class Meta:
        model = VerifInvalidGeometry
        attrs = {'class': 'green'}
        
def invalid_proj (request):
    upc = VerifProjection.objects.all()
    table = invalid_projTable(VerifProjection.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=500)
    RequestConfig(request,paginate={'per_page': 500}).configure(table)
    return render(request,'verif_invalid_proj.html',{'inv_proj':table})
# Create your views here.

class invalid_projTable(tables.Table):
    class Meta:
        model = VerifProjection
        attrs = {'class': 'green'}
        
def count_meshWithoutLandUseArea (request):
    upc = VerifFieldMesh.objects.all()
    table = meshWithoutAPTable(VerifFieldMesh.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=500)
    RequestConfig(request,paginate={'per_page': 500}).configure(table)
    return render(request,'ctrainte_field_specificMesh_without_LandUseArea.html',{'count_error':table})
# Create your views here.

class meshWithoutAPTable(tables.Table):
    class Meta:
        model = VerifFieldMesh
        attrs = {'class': 'green'}
        
def count_HouseholdWithoutAbstractPerson (request):
    upc = VerifHousehold.objects.all()
    table = hhWithoutAPTable(VerifHousehold.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=500)
    RequestConfig(request,paginate={'per_page': 500}).configure(table)
    return render(request,'ctrainte_Household_without_AP.html',{'count_error':table})
# Create your views here.

class hhWithoutAPTable(tables.Table):
    class Meta:
        model = VerifHousehold
        attrs = {'class': 'green'}
        
