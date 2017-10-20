#-*- coding: utf-8 -*-
#!/usr/bin/env python3
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponseRedirect


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
from stat_cc_idf.models import countStatistiques
from stat_cc_idf.forms import ContactForm
from stat_cc_idf.model_params import MODEL_CONFIG_PARAMS_FUNCTION



# from launch_UpdData import * 
import stat_cc_idf.launch_UpdData as launch_UpdData
import stat_cc_idf.model_params as model_params




          
def date_actuelle(request):
    return render(request, 'date.html', {'date': datetime.now()})
    
def cartoCC(request):
    return render(request, 'cartoCC.html', {})
    
def accueil(request):
    # Construire le formulaire, soit avec les données postées,
    # soit vide si l'utilisateur accède pour la première fois
    # à la page.
    form = ContactForm(request.POST or None)
    # Nous vérifions que les données envoyées sont valides
    # Cette méthode renvoie False s'il n'y a pas de données 
    # dans le formulaire ou qu'il contient des erreurs.
    if form.is_valid(): 
        # Ici nous pouvons traiter les données du formulaire
        host = form.cleaned_data['host']
        db_name = form.cleaned_data['db_name']
        user = form.cleaned_data['user']
        password = form.cleaned_data['password']
        city_context_name = form.cleaned_data['city_context_name']
        model_params.MODEL_BDD_PARAMS['credentials']['host'] = host
        model_params.MODEL_BDD_PARAMS['credentials']['dbname'] = db_name
        model_params.MODEL_BDD_PARAMS['credentials']['user'] = user
        model_params.MODEL_BDD_PARAMS['credentials']['password'] = password
        print('cc name : ' + str(model_params.MODEL_BDD_PARAMS['city_context_name'][0]))
        print('cc name Form : ' + str(city_context_name))
        model_params.MODEL_BDD_PARAMS['city_context_name'][0] = city_context_name
        # Nous pourrions ici envoyer l'e-mail grâce aux données 
        # que nous venons de récupérer
        envoi = True
        # print ( str(model_params.MODEL_BDD_PARAMS['city_context_name'][0]))
        # print model_params.MODEL_CONFIG_PARAMS_FUNCTION(model_params.MODEL_BDD_PARAMS)['Requests']['Request_field_mesh']
    return render(request, 'accueil.html', {'form':form})
   
def NbEntites(request):
    nbEntites = VerifNombreEntites.objects.all()
    # Type_Object=request.GET.get('Type_Object')
    # table = EntiteTable(VerifNombreEntites.objects.filter(type_object=Type_Object))
    table = EntiteTable(VerifNombreEntites.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=500)
    RequestConfig(request,paginate={'per_page': 500}).configure(table)
    return render(request,'stat_NombreEntites.html',{'nb_ent':table})
    

class EntiteTable(tables.Table):
    class Meta:
        model = VerifNombreEntites
        attrs = {'class': 'palegreen'}
        
def urban_project_capacity(request):
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
    table = Ind_sectorTable(VerifTypeInductrySector.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=500)
    RequestConfig(request,paginate={'per_page': 500}).configure(table)
    return render(request,'categories_IndustrySector.html',{'cat_indSector':table})

class Ind_sectorTable(tables.Table):
    class Meta:
        model = VerifTypeInductrySector
        attrs = {'class': 'green'}
        
def count_stat(request):
    table = countStatistiquesTable(countStatistiques.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=500)
    RequestConfig(request,paginate={'per_page': 500}).configure(table)
    return render(request,'countStatistiques.html',{'countStat':table})

class countStatistiquesTable(tables.Table):
    class Meta:
        model = countStatistiques
        attrs = {'class': 'green'}
        
def invalid_geom (request):
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
    table = invalid_projTable(VerifProjection.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=500)
    RequestConfig(request,paginate={'per_page': 500}).configure(table)
    return render(request,'verif_invalid_proj.html',{'inv_proj':table})
# Create your views here.

class invalid_projTable(tables.Table):
    class Meta:
        model = VerifProjection
        attrs = {'class': 'green'}
                
def count_contraintesIntegrite (request):
    tableHH = hhWithoutAPTable(VerifHousehold.objects.all())
    tableMesh = meshWithoutAPTable(VerifFieldMesh.objects.all())
    tableHH.paginate(page=request.GET.get('page', 1), per_page=500)
    tableMesh.paginate(page=request.GET.get('page', 1), per_page=500)
    RequestConfig(request,paginate={'per_page': 500}).configure(tableHH)
    RequestConfig(request,paginate={'per_page': 500}).configure(tableMesh)
    return render(request,'contraintes.html',{'count_Mesh':tableMesh, 'count_HH':tableHH})
# Create your views here.

def selected_path(request):
    if(request.GET.get('mybtn')):
        counter = 8
        # print counter    
    return render(request, 'selected_path.html', {'selected_path':counter}) 

def output(request):
    if request.is_ajax():
        py_obj = test_code(10)
        return render(request, 'output.html', {'output': py_obj.a})

class hhWithoutAPTable(tables.Table):
    class Meta:
        model = VerifHousehold
        attrs = {'class': 'green'}

class meshWithoutAPTable(tables.Table):
    class Meta:
        model = VerifFieldMesh
        attrs = {'class': 'green'}


def launch_UpdData1(request):
    res1 = launch_UpdData.launch_UpdData('verif_nombre_entites',model_params.MODEL_CONFIG_PARAMS_FUNCTION(model_params.MODEL_BDD_PARAMS)['Requests']['Request_count'],model_params.MODEL_CONFIG_PARAMS_FUNCTION(model_params.MODEL_BDD_PARAMS)['Requests_params']['Request_insert_count'])
    return render(request, 'accueil.html', {'res1' : res1})
def launch_UpdData2(request):
    res2 = launch_UpdData.launch_UpdData('verif_urban_project_capacity',model_params.MODEL_CONFIG_PARAMS_FUNCTION(model_params.MODEL_BDD_PARAMS)['Requests']['Request_urban_city'],model_params.MODEL_CONFIG_PARAMS_FUNCTION(model_params.MODEL_BDD_PARAMS)['Requests_params']['Request_insert_urban_city'])
    return render(request, 'accueil.html', {'res2' : res2})
def launch_UpdData3(request):
    res3 = launch_UpdData.launch_UpdData('verif_type_inductry_sector',model_params.MODEL_CONFIG_PARAMS_FUNCTION(model_params.MODEL_BDD_PARAMS)['Requests']['Request_type_sector'],model_params.MODEL_CONFIG_PARAMS_FUNCTION(model_params.MODEL_BDD_PARAMS)['Requests_params']['Request_insert_type_sector'])
    return render(request, 'accueil.html', {'res3' : res3})
def launch_UpdData4(request):
    res4 = launch_UpdData.launch_UpdData('verif_invalid_geometry',model_params.MODEL_CONFIG_PARAMS_FUNCTION(model_params.MODEL_BDD_PARAMS)['Requests']['Request_invalid_geometry'],model_params.MODEL_CONFIG_PARAMS_FUNCTION(model_params.MODEL_BDD_PARAMS)['Requests_params']['Request_insert_invalid_geometry'])
    return render(request, 'accueil.html', {'res4' : res4})
def launch_UpdData5(request):
    res5 = launch_UpdData.launch_UpdData('verif_projection',model_params.MODEL_CONFIG_PARAMS_FUNCTION(model_params.MODEL_BDD_PARAMS)['Requests']['Request_projection_verif'],model_params.MODEL_CONFIG_PARAMS_FUNCTION(model_params.MODEL_BDD_PARAMS)['Requests_params']['Request_insert_projection_verif'])
    return render(request, 'accueil.html', {'res5' : res5})
def launch_UpdData6(request):
    res6 = launch_UpdData.launch_UpdData_constraint_tables('verif_field_mesh',model_params.MODEL_CONFIG_PARAMS_FUNCTION(model_params.MODEL_BDD_PARAMS)['Requests']['Request_field_mesh'],model_params.MODEL_CONFIG_PARAMS_FUNCTION(model_params.MODEL_BDD_PARAMS)['Requests_params']['Request_insert_field_mesh'])
    return render(request, 'accueil.html', {'res6' : res6})
def launch_UpdData7(request):
    res7 = launch_UpdData.launch_UpdData_constraint_tables('verif_household',model_params.MODEL_CONFIG_PARAMS_FUNCTION(model_params.MODEL_BDD_PARAMS)['Requests']['Request_household'],model_params.MODEL_CONFIG_PARAMS_FUNCTION(model_params.MODEL_BDD_PARAMS)['Requests_params']['Request_insert_household'])
    return render(request, 'accueil.html', {'res7' : res7})
def launch_UpdData8(request):
    res8 = launch_UpdData.launch_UpdData_stat('verif_count_statistics',[model_params.MODEL_CONFIG_PARAMS_FUNCTION(model_params.MODEL_BDD_PARAMS)['Requests']['Request_count_household'],model_params.MODEL_CONFIG_PARAMS_FUNCTION(model_params.MODEL_BDD_PARAMS)['Requests']['Request_employment']],model_params.MODEL_CONFIG_PARAMS_FUNCTION(model_params.MODEL_BDD_PARAMS)['Requests_params']['Request_insert_into_count_statistics'])
    return render(request, 'accueil.html', {'res8' : res8})

def launch_UpdAllData(request):

    start_time = datetime.now()
    #connection to city_context
    cur = connection.cursor()
    #connection to verif_shema
    target_cur = target_connection.cursor()
    #delete all table content
    try:
        target_cur.execute("TRUNCATE {0}.verif_nombre_entites, {0}.verif_urban_project_capacity, {0}.verif_type_inductry_sector, {0}.verif_invalid_geometry, {0}.verif_projection;" .format(MODEL_BDD_PARAMS['verif_quality_schema']))
        target_connection.commit() 
    except Exception as e:
        print ("erreur :" + str(e)) 
    #execute 1st request
    array_values = exec_request(cur,model_params.MODEL_CONFIG_PARAMS['Requests']['Request_count'])
    #insert for 1st request 
    insert_into(array_values,target_cur,model_params.MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_count'])
    first_request_time = datetime.now()
    print("Count Request done in %s seconds!" %(first_request_time-start_time))
    #execute 2nd request      
    array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_urban_city'])
    #insert for 2nd request
    insert_into(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_urban_city'])
    second_request_time = datetime.now()  
    print("Urban_city Request done in %s seconds!" %(second_request_time - first_request_time))
    #execute 3rd request
    array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_type_sector'])
    #insert for 3rd request
    insert_into(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_type_sector'])
    third_request_time = datetime.now()
    print("Type_sector Request done in %s seconds!" %(third_request_time - second_request_time))
    #execute geometry request
    array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_invalid_geometry'])
    #insert invalid_geometry
    insert_into(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_invalid_geometry'])
    fourth_request_time = datetime.now()
    print("Invalid_geometry Request done in %s seconds!" %(fourth_request_time - third_request_time))
    #execute projection request
    array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_projection_verif'])
    #insert projection verif
    insert_into(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_projection_verif'])
    fifth_request_time = datetime.now()
    print("Projection_verif Request done in %s seconds!" %(fifth_request_time - fourth_request_time))
    #execute integrity constraint
    array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_field_mesh'])
    #insert integrity_constraint
    insert_into_constraint_tables(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_field_mesh'])
    six_request_time = datetime.now()
    print("Mesh_without_area Request done in %s seconds!" %(six_request_time - fifth_request_time))
    #execute household request
    array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_household'])
    #insert household request
    insert_into_constraint_tables(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_household'])
    final_time = datetime.now()
    #target_connection commit
    target_connection.commit()
    res = ("household Request done in %s seconds!" %(final_time - start_time))
    print("commit ok. All data loaded successfully")
    return render(request, 'accueil.html', {'res8' : res})        