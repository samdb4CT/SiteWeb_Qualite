#-*- coding: utf-8 -*-
#Model parameters
MODEL_BDD_PARAMS = {
    'credentials': {
        'host': '192.168.1.130',
        'dbname': 'cc_dynex_idf_test',
        'user': 's_deschamps',
        'password': 's_deschampsberger',
    },
    'credentials_db_target': {
        'host': '192.168.1.130',
        'dbname': 'integration_france',
        'user': 's_deschamps',
        'password': 's_deschampsberger'   
    },
    'city_context_name' : ['\"e7fd873b-38e5-41c8-834f-26d41d845493\"'],
    'verif_quality_schema' : 'aaa_qualite_donnees',
    }

#config requests  
def MODEL_CONFIG_PARAMS_FUNCTION(MODEL_BDD_PARAMS):  
    MODEL_CONFIG_PARAMS = {
        'Requests': {
            'Request_count': "SELECT 'base' as type_object, city_object_type, count(*), \'{0}\'::varchar as cc_name from {0}.city_objects group by city_object_type union select 'extension' as type_object, city_object_extension_type, count(*),\'{0}\'::varchar as cc_name from {0}.city_object_extensions group by city_object_extension_type " .format(MODEL_BDD_PARAMS['city_context_name'][0]),
            # 'Request_urban_city': "SELECT object_id, data->>'area' as area, data->'classification'->>'usage' AS usage,  \'{0}\' as cc_name  FROM (SELECT object_id, jsonb_array_elements(data->'floor_areas') AS data, validity_range FROM {0}.city_object_extensions WHERE city_object_extension_type='urban_project_capacity') AS sub WHERE data->>'area'!= {1} " .format(MODEL_BDD_PARAMS['city_context_name'][0], '\'{"unit": "m^{2}", "value": 0}\''),
            'Request_urban_city': "SELECT object_id, concat(data->'area'->>'value',' ',data->'area'->>'unit') as area, data->'classification'->>'usage' AS usage,  \'{0}\'::varchar as cc_name FROM (SELECT object_id, jsonb_array_elements(data->'floor_areas') AS data, validity_range FROM {0}.city_object_extensions WHERE city_object_extension_type='urban_project_capacity') AS sub WHERE data->>'area'!= {1} " .format(MODEL_BDD_PARAMS['city_context_name'][0], '\'{"unit": "m^{2}", "value": 0}\''),
            'Request_type_sector': "SELECT zone, cast(jobs->>'value' AS INTEGER) as value, jobs->'classification'->>'industry_sector' AS sector,  \'{0}\'::varchar as cc_name  FROM ( SELECT object_id AS zone, jsonb_array_elements(data -> 'number_of_jobs') AS jobs FROM {0}.city_object_extensions WHERE city_object_extension_type='employment') AS sub" .format(MODEL_BDD_PARAMS['city_context_name'][0]),
            'Request_invalid_geometry': "SELECT st_isvalid(geometry), object_id, city_object_type , \'{0}\'::varchar as cc_name FROM {0}.city_objects WHERE city_object_type='field_specific_mesh' AND not st_isvalid(geometry)" .format(MODEL_BDD_PARAMS['city_context_name'][0]),
            'Request_projection_verif': "SELECT distinct st_srid(geometry) , \'{0}\'::varchar as cc_name FROM {0}.city_objects where  st_srid(geometry) != {1}" .format(MODEL_BDD_PARAMS['city_context_name'][0], 4326),
            'Request_field_mesh': "SELECT count(tp.lua_id), \'{0}\'::varchar as cc_name from (select lua.object_id as lua_id from (select object_id from {0}.city_object_extensions where city_object_extension_type = 'land_use_areas') as lua right join (select object_id from {0}.city_objects where city_object_type = 'field_specific_mesh') as fsm on fsm.object_id = lua.object_id where lua.object_id is null) as tp" .format(MODEL_BDD_PARAMS['city_context_name'][0]),
            'Request_household' : "SELECT count(tp.id_hhd), \'{0}\'::varchar as cc_name  from (select hhd.object_id as id_hhd from (select object_id from {0}.city_object_extensions where city_object_extension_type = 'household_abstract_persons' ) as ap left join (select object_id from {0}.city_objects where city_object_type = 'household' ) as hhd on hhd.object_id = ap.object_id where hhd.object_id is null) as tp" .format(MODEL_BDD_PARAMS['city_context_name'][0]),
            'Request_employment' : "SELECT 'nb_employments'::varchar  as nom, sum((jobs.caracteristics->>'value')::int) as count, \'{0}\'::varchar as cc_name from ( select object_id, jsonb_array_elements(data->'number_of_jobs') as caracteristics from {0}.city_object_extensions where city_object_extension_type = 'employment' AND object_id NOT LIKE 'TERRITOR%' ) as jobs" .format(MODEL_BDD_PARAMS['city_context_name'][0]),
            'Request_count_household' : "SELECT 'nb_households'::varchar as nom, count(object_id), \'{0}\'::varchar as cc_name from {0}.city_object_extensions where city_object_extension_type = 'household_abstract_persons'".format(MODEL_BDD_PARAMS['city_context_name'][0])
        },
        'Requests_params' : {
            'Request_insert_count': "INSERT INTO {0}.verif_nombre_entites (type_object,city_object_type,count, cc_name)".format(MODEL_BDD_PARAMS['verif_quality_schema']),
            'Request_insert_urban_city': "INSERT INTO {0}.verif_urban_project_capacity (object_id,area,usage, cc_name)" .format(MODEL_BDD_PARAMS['verif_quality_schema']),
            'Request_insert_type_sector': "INSERT INTO {0}.verif_type_inductry_sector (zone,value,sector, cc_name)" .format(MODEL_BDD_PARAMS['verif_quality_schema']),
            'Request_insert_invalid_geometry': "INSERT INTO {0}.verif_invalid_geometry (st_isvalid,object_id,city_object_type, cc_name)" .format(MODEL_BDD_PARAMS['verif_quality_schema']),
            'Request_insert_projection_verif': "INSERT INTO {0}.verif_projection (st_srid,object_id,city_object_type, cc_name)" .format(MODEL_BDD_PARAMS['verif_quality_schema']),
            'Request_insert_field_mesh': "INSERT INTO {0}.verif_field_mesh (count, cc_name)" .format(MODEL_BDD_PARAMS['verif_quality_schema']),
            'Request_insert_household': "INSERT INTO {0}.verif_household(count, cc_name)" .format(MODEL_BDD_PARAMS['verif_quality_schema']),
            'Request_insert_into_count_statistics' : "INSERT INTO {0}.count_statistics(nom, count,cc_name)" .format(MODEL_BDD_PARAMS['verif_quality_schema'])
        }
    }
    return MODEL_CONFIG_PARAMS    