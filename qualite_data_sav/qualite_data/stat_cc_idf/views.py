#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import Http404
from datetime import datetime
import psycopg2
import numpy as np
import time

import django_tables2 as tables
from django_tables2 import RequestConfig
from stat_cc_idf.models import VerifNombreEntites
from stat_cc_idf.models import VerifUrbanProjectCapacity
from stat_cc_idf.models import VerifTypeInductrySector
from stat_cc_idf.models import VerifInvalidGeometry
from stat_cc_idf.models import VerifProjection
from stat_cc_idf.models import VerifFieldMesh
from stat_cc_idf.models import VerifHousehold

#Model parameters
MODEL_BDD_PARAMS = {
    'credentials': {
        'host': '192.168.1.130',
        'dbname': 'cc_dynex_idf_test',
        'user': 's_deschamps',
        'password': 's_deschampsberger'
    },
    'credentials_db_target': {
        'host': '192.168.1.130',
        'dbname': 'integration_france',
        'user': 's_deschamps',
        'password': 's_deschampsberger'   
    },
    'city_context_name' : '\"e7fd873b-38e5-41c8-834f-26d41d845493\"',
    'verif_quality_schema' : 'aaa_qualite_donnees',
    }

#config requests    
MODEL_CONFIG_PARAMS = {
    'Requests': {
        'Request_count': "SELECT 'base' as type_object, city_object_type, count(*) from {0}.city_objects group by city_object_type union select 'extension' as type_object, city_object_extension_type, count(*) from {0}.city_object_extensions group by city_object_extension_type " .format(MODEL_BDD_PARAMS['city_context_name']),
        'Request_urban_city': "SELECT object_id, data->>'area' as area, data->'classification'->>'usage' AS usage FROM (SELECT object_id, jsonb_array_elements(data->'floor_areas') AS data, validity_range FROM {0}.city_object_extensions WHERE city_object_extension_type='urban_project_capacity') AS sub WHERE data->>'area'!= {1} " .format(MODEL_BDD_PARAMS['city_context_name'], '\'{"unit": "m^{2}", "value": 0}\''),
        'Request_type_sector': "SELECT zone, cast(jobs->>'value' AS INTEGER) as value, jobs->'classification'->>'industry_sector' AS sector FROM ( SELECT object_id AS zone, jsonb_array_elements(data -> 'number_of_jobs') AS jobs FROM {0}.city_object_extensions WHERE city_object_extension_type='employment') AS sub" .format(MODEL_BDD_PARAMS['city_context_name']),
        'Request_invalid_geometry': "SELECT st_isvalid(geometry), object_id, city_object_type FROM {0}.city_objects WHERE city_object_type='field_specific_mesh' AND not st_isvalid(geometry)" .format(MODEL_BDD_PARAMS['city_context_name']),
        'Request_projection_verif': "SELECT distinct st_srid(geometry) FROM {0}.city_objects where  st_srid(geometry) != {1}" .format(MODEL_BDD_PARAMS['city_context_name'], 4326),
        'Request_field_mesh': "SELECT count(tp.lua_id) from (select lua.object_id as lua_id from (select object_id from {0}.city_object_extensions where city_object_extension_type = 'land_use_areas') as lua right join (select object_id from {0}.city_objects where city_object_type = 'field_specific_mesh') as fsm on fsm.object_id = lua.object_id where lua.object_id is null) as tp" .format(MODEL_BDD_PARAMS['city_context_name']),
        'Request_household' : "SELECT count(tp.id_hhd) from (select hhd.object_id as id_hhd from (select object_id from {0}.city_object_extensions where city_object_extension_type = 'household_abstract_persons' ) as ap left join (select object_id from {0}.city_objects where city_object_type = 'household' ) as hhd on hhd.object_id = ap.object_id where hhd.object_id is null) as tp" .format(MODEL_BDD_PARAMS['city_context_name'])
    },
    'Requests_params' : {
        'Request_insert_count': "INSERT INTO {0}.verif_nombre_entites (type_object,city_object_type,count)".format(MODEL_BDD_PARAMS['verif_quality_schema']),
        'Request_insert_urban_city': "INSERT INTO {0}.verif_urban_project_capacity (object_id,area,usage)" .format(MODEL_BDD_PARAMS['verif_quality_schema']),
        'Request_insert_type_sector': "INSERT INTO {0}.verif_type_inductry_sector (zone,value,sector)" .format(MODEL_BDD_PARAMS['verif_quality_schema']),
        'Request_insert_invalid_geometry': "INSERT INTO {0}.verif_invalid_geometry (st_isvalid,object_id,city_object_type)" .format(MODEL_BDD_PARAMS['verif_quality_schema']),
        'Request_insert_projection_verif': "INSERT INTO {0}.verif_projection (st_srid,object_id,city_object_type)" .format(MODEL_BDD_PARAMS['verif_quality_schema']),
        'Request_insert_field_mesh': "INSERT INTO {0}.verif_field_mesh (count)" .format(MODEL_BDD_PARAMS['verif_quality_schema']),
        'Request_insert_household': "INSERT INTO {0}.verif_household(count)" .format(MODEL_BDD_PARAMS['verif_quality_schema']),
    }
}
try:
    print('Connecting to %s DB (%s)...' % (MODEL_BDD_PARAMS['credentials']['dbname'], MODEL_BDD_PARAMS['credentials']['host']))
    connection = psycopg2.connect(' '.join(['%s=%s' %(key, value) for key, value in MODEL_BDD_PARAMS['credentials'].items()]))
except Exception as e:
    print("I am unable to connect to the database.")
    print(str(e))

try:
    print('Connecting to %s DB (%s)...' % (MODEL_BDD_PARAMS['credentials_db_target']['dbname'], MODEL_BDD_PARAMS['credentials_db_target']['host']))
    target_connection = psycopg2.connect(' '.join(['%s=%s' %(key, value) for key, value in MODEL_BDD_PARAMS['credentials_db_target'].items()]))
except:
    print("Unable to connect to the database.")
print("connection established, requests starting, may took a while...")

def exec_request(cursor,request):
        try:
            cursor.execute(request)
        except Exception as a:
            print(a)
        rows = cursor.fetchall()
        array_values = np.asarray(rows)

        return array_values

def insert_into(array,cursor,request):
    for x in array:
        try:       
            cursor.execute("""
                %s
                VALUES ('%s','%s','%s') """ % (request,x[0],x[1],x[2])
          
                )
        except psycopg2.ProgrammingError as a:
            print(a)

def insert_into_constraint_tables(array,cursor,request):
    for x in array:
        try:       
            cursor.execute("""
                %s
                VALUES ('%s') """ % (request,x[0])
          
                )
        except psycopg2.ProgrammingError as a:
            print(a)

def date_actuelle(request):
    return render(request, 'date.html', {'date': datetime.now()})
    
def cartoCC(request):
    return render(request, 'cartoCC.html', {})
    
def accueil(request):
    return render(request, 'accueil.html', {})
    
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
# Create your views here.

class Ind_sectorTable(tables.Table):
    class Meta:
        model = VerifTypeInductrySector
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

class hhWithoutAPTable(tables.Table):
    class Meta:
        model = VerifHousehold
        attrs = {'class': 'green'}

class meshWithoutAPTable(tables.Table):
    class Meta:
        model = VerifFieldMesh
        attrs = {'class': 'green'}
        


def launch_UpdData1(request):

    start_time = time.time()
    #connection to city_context
    cur = connection.cursor()
    #connection to verif_shema
    target_cur = target_connection.cursor()
    #delete all table content
    target_cur.execute("TRUNCATE {0}.verif_nombre_entites" .format(MODEL_BDD_PARAMS['verif_quality_schema']))
    target_connection.commit() 
    #execute 1st request
    array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_count'])
    # insert for 1st request 
    insert_into(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_count'])
    first_request_time = time.time()
    print ( "Count Request done in %s seconds!" %(first_request_time- start_time))
    res1 = ("Count Request done in %s seconds!" %(first_request_time- start_time))
    #target_connection commit
    target_connection.commit()
    print("commit ok. All data loaded successfully")
    return render(request, 'accueil.html', {'res1' : res1})

def launch_UpdData2(request):

    start_time = time.time()
    #connection to city_context
    cur = connection.cursor()
    #connection to verif_shema
    target_cur = target_connection.cursor()
    #delete all table content
    target_cur.execute("TRUNCATE {0}.verif_urban_project_capacity" .format(MODEL_BDD_PARAMS['verif_quality_schema']))
    target_connection.commit()   
    #execute 2nd request      
    array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_urban_city'])
    #insert for 2nd request
    insert_into(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_urban_city'])
    second_request_time = time.time()  
    print ( "Urban_city Request done in %s seconds!" %(second_request_time - start_time))
    res2 = ("Urban_city Request done in %s seconds!" %(second_request_time - start_time))
    #target_connection commit
    target_connection.commit()
    print("commit ok. All data loaded successfully")
    return render(request, 'accueil.html', {'res2' : res2})

def launch_UpdData3(request):

    start_time = time.time()
    #connection to city_context
    cur = connection.cursor()
    #connection to verif_shema
    target_cur = target_connection.cursor()
    #delete all table content
    target_cur.execute("TRUNCATE {0}.verif_type_inductry_sector" .format(MODEL_BDD_PARAMS['verif_quality_schema']))
    target_connection.commit()   
    #execute 3rd request
    array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_type_sector'])
    #insert for 3rd request
    insert_into(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_type_sector'])
    third_request_time = time.time()
    print( "Type_sector Request done in %s seconds!" %(third_request_time - start_time))
    res3 = ("Type_Sector Request done in %s seconds!" %(third_request_time - start_time))
    #target_connection commit
    target_connection.commit()
    print("commit ok. All data loaded successfully")
    return render(request, 'accueil.html', {'res3' : res3})

def launch_UpdData4(request):

    start_time = time.time()
    #connection to city_context
    cur = connection.cursor()
    #connection to verif_shema
    target_cur = target_connection.cursor()
    #delete all table content
    target_cur.execute("TRUNCATE {0}.verif_invalid_geometry" .format(MODEL_BDD_PARAMS['verif_quality_schema']))
    target_connection.commit()  
    #execute geometry request
    array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_invalid_geometry'])
    #insert invalid_geometry
    insert_into(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_invalid_geometry'])
    fourth_request_time = time.time()
    print( "Invalid_geometry Request done in %s seconds!" %(fourth_request_time - start_time))
    res4 = ("Type_Sector Request done in %s seconds!" %(fourth_request_time - start_time))
    #target_connection commit
    target_connection.commit()
    print("commit ok. All data loaded successfully")
    return render(request, 'accueil.html', {'res4' : res4})

def launch_UpdData5(request):
    
    start_time = time.time()
    #connection to city_context
    cur = connection.cursor()
    #connection to verif_shema
    target_cur = target_connection.cursor()
    #delete all table content
    target_cur.execute("TRUNCATE {0}.verif_projection" .format(MODEL_BDD_PARAMS['verif_quality_schema']))
    target_connection.commit()     
    #execute projection request
    array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_projection_verif'])
    #insert projection verif
    insert_into(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_projection_verif'])
    fifth_request_time = time.time()
    print( "Projection_verif Request done in %s seconds!" %(fifth_request_time - start_time))
    res5 = ("Projection_verif Request done in %s seconds!" %(fifth_request_time - start_time))
    #target_connection commit
    target_connection.commit()
    print("commit ok. All data loaded successfully")
    return render(request, 'accueil.html', {'res5' : res5})

def launch_UpdData6(request):

    print ("je rentre dedans")
    start_time = time.time()
    #connection to city_context
    cur = connection.cursor()
    #connection to verif_shema
    target_cur = target_connection.cursor()
    #delete all table content
    target_cur.execute("TRUNCATE {0}.verif_field_mesh" .format(MODEL_BDD_PARAMS['verif_quality_schema']))
    target_connection.commit()  
    #execute integrity constraint
    array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_field_mesh'])
    #insert integrity_constraint
    insert_into_constraint_tables(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_field_mesh'])
    six_request_time = time.time()
    print( "Mesh_without_area Request done in %s seconds!" %(six_request_time - start_time))
    res6 = ("Mesh_without_area  Request done in %s seconds!" %(six_request_time - start_time))
    #target_connection commit
    target_connection.commit()
    print("commit ok. All data loaded successfully")
    return render(request, 'accueil.html', {'res6' : res6})

def launch_UpdData7(request):

    start_time = time.time()
    #connection to city_context
    cur = connection.cursor()
    #connection to verif_shema
    target_cur = target_connection.cursor()
    #delete all table content
    target_cur.execute("TRUNCATE {0}.verif_household" .format(MODEL_BDD_PARAMS['verif_quality_schema']))
    target_connection.commit()     
    #execute household request
    array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_household'])
    #insert household request
    insert_into_constraint_tables(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_household'])
    seven_request_time = time.time()
    print( "household Request done in %s seconds!" %(seven_request_time - start_time))
    res7 = ("household Request done in %s seconds!" %(seven_request_time - six_request_time))
    #target_connection commit
    target_connection.commit()
    print("commit ok. All data loaded successfully")
    return render(request, 'accueil.html', {'res7' : res7})

def launch_UpdAllData(request):

    start_time = time.time()
    #connection to city_context
    cur = connection.cursor()
    #connection to verif_shema
    target_cur = target_connection.cursor()
    #delete all table content
    target_cur.execute("TRUNCATE {0}.verif_nombre_entites, {0}.verif_urban_project_capacity, {0}.verif_type_inductry_sector, {0}.verif_invalid_geometry, {0}.verif_projection;" .format(MODEL_BDD_PARAMS['verif_quality_schema']))
    target_connection.commit() 
    #execute 1st request
    array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_count'])
    #insert for 1st request 
    insert_into(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_count'])
    first_request_time = time.time()
    print("Count Request done in %s seconds!" %(first_request_time-start_time))
    #execute 2nd request      
    array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_urban_city'])
    #insert for 2nd request
    insert_into(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_urban_city'])
    second_request_time = time.time()  
    print("Urban_city Request done in %s seconds!" %(second_request_time - first_request_time))
    #execute 3rd request
    array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_type_sector'])
    #insert for 3rd request
    insert_into(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_type_sector'])
    third_request_time = time.time()
    print("Type_sector Request done in %s seconds!" %(third_request_time - second_request_time))
    #execute geometry request
    array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_invalid_geometry'])
    #insert invalid_geometry
    insert_into(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_invalid_geometry'])
    fourth_request_time = time.time()
    print("Invalid_geometry Request done in %s seconds!" %(fourth_request_time - third_request_time))
    #execute projection request
    array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_projection_verif'])
    #insert projection verif
    insert_into(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_projection_verif'])
    fifth_request_time = time.time()
    print("Projection_verif Request done in %s seconds!" %(fifth_request_time - fourth_request_time))
    #execute integrity constraint
    array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_field_mesh'])
    #insert integrity_constraint
    insert_into_constraint_tables(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_field_mesh'])
    six_request_time = time.time()
    print("Mesh_without_area Request done in %s seconds!" %(six_request_time - fifth_request_time))
    #execute household request
    array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_household'])
    #insert household request
    insert_into_constraint_tables(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_household'])
    final_time = time.time()
    #target_connection commit
    target_connection.commit()
    res8 = ("household Request done in %s seconds!" %(final_time - start_time))
    print("commit ok. All data loaded successfully")
    return render(request, 'accueil.html', {'res8' : res8})        