#!/usr/bin/env Python
# -*- coding: utf8 -*-

import psycopg2
import numpy as np
import time

class updData:
    #Model parameters
    MODEL_BDD_PARAMS = {
        'credentials': {
            'host': '192.168.1.130',
            'dbname': 'cc_dynex_idf_test',
            'user': 'n_delory',
            'password': 'n_delory20022017'
        },
        'credentials_db_target': {
            'host': '192.168.1.130',
            'dbname': 'integration_france',
            'user': 'n_delory',
            'password': 'n_delory20022017'   
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

    def exec_request(cursor,request):
        try:

            cursor.execute(request)
        except psycopg2.ProgrammingError as a:
            print a
        rows = cur.fetchall()
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
                print a

    def insert_into_constraint_tables(array,cursor,request):
        for x in array:
            try:       
                cursor.execute("""
                    %s
                    VALUES ('%s') """ % (request,x[0])
              
                    )
            except psycopg2.ProgrammingError as a:
                print a



    #connections to DB
    def init():
        try:
            print 'Connecting to %s DB (%s)...' % (MODEL_BDD_PARAMS['credentials']['dbname'], MODEL_BDD_PARAMS['credentials']['host'])
            connection = psycopg2.connect(' '.join(['%s=%s' %(key, value) for key, value in MODEL_BDD_PARAMS['credentials'].iteritems()]))
        except:
            print "I am unable to connect to the database."

        try:
            print 'Connecting to %s DB (%s)...' % (MODEL_BDD_PARAMS['credentials_db_target']['dbname'], MODEL_BDD_PARAMS['credentials_db_target']['host'])
            target_connection = psycopg2.connect(' '.join(['%s=%s' %(key, value) for key, value in MODEL_BDD_PARAMS['credentials_db_target'].iteritems()]))
        except:
            print "Unable to connect to the database."

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
        print "Count Request done in %s seconds!" %(first_request_time-start_time)
        #execute 2nd request      
        array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_urban_city'])
        #insert for 2nd request
        insert_into(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_urban_city'])
        second_request_time = time.time()  
        print "Urban_city Request done in %s seconds!" %(second_request_time - first_request_time)
        #execute 3rd request
        array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_type_sector'])
        #insert for 3rd request
        insert_into(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_type_sector'])
        third_request_time = time.time()
        print "Type_sector Request done in %s seconds!" %(third_request_time - second_request_time)
        #execute geometry request
        array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_invalid_geometry'])
        #insert invalid_geometry
        insert_into(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_invalid_geometry'])
        fourth_request_time = time.time()
        print "Invalid_geometry Request done in %s seconds!" %(fourth_request_time - third_request_time)
        #execute projection request
        array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_projection_verif'])
        #insert projection verif
        insert_into(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_projection_verif'])
        fifth_request_time = time.time()
        print "Projection_verif Request done in %s seconds!" %(fifth_request_time - fourth_request_time)
        #execute integrity constraint
        array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_field_mesh'])
        #insert integrity_constraint
        insert_into_constraint_tables(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_field_mesh'])
        six_request_time = time.time()
        print "Mesh_without_area Request done in %s seconds!" %(six_request_time - fifth_request_time)
        #execute household request
        array_values = exec_request(cur,MODEL_CONFIG_PARAMS['Requests']['Request_household'])
        #insert household request
        insert_into_constraint_tables(array_values,target_cur,MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_household'])

        #target_connection commit
        target_connection.commit()    
    