#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import time
import stat_cc_idf.model_params as model_params
import psycopg2
import numpy as np


connection = psycopg2.connect(' '.join(['%s=%s' %(key, value) for key, value in model_params.MODEL_BDD_PARAMS['credentials'].items()]))
target_connection = psycopg2.connect(' '.join(['%s=%s' %(key, value) for key, value in model_params.MODEL_BDD_PARAMS['credentials_db_target'].items()]))



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
                VALUES ('%s','%s','%s','%s') """ % (request,x[0],x[1],x[2],x[3])
          
                )
        except psycopg2.ProgrammingError as a:
            print(a)

def insert_into_constraint_tables(array,cursor,request):
    for x in array:
        try:       
            cursor.execute("""
                %s
                VALUES ('%s','%s') """ % (request,x[0],x[1])
          
                )
        except psycopg2.ProgrammingError as a:
            print(a)
def insert_into_statistics_table(array,cursor,request):
    for x in array:
        try:       
            cursor.execute("""
                %s
                VALUES ('%s','%s','%s') """ % (request,x[0],x[1],x[2])
          
                )
        except psycopg2.ProgrammingError as a:
            print(a) 

def launch_UpdData(table_to_truncate,request,table_to_insert):
    start_time = time.time()
    #connection to city_context
    cur = connection.cursor()
    #connection to verif_shema
    target_cur = target_connection.cursor()
    #delete all table content
    try:
        target_cur.execute("TRUNCATE {0}.{1}" .format(model_params.MODEL_BDD_PARAMS['verif_quality_schema'],table_to_truncate))
        target_connection.commit() 
    except Exception as e:
        print ("erreur :" + str(e)) 
    #execute 1st request
    array_values = exec_request(cur,request)
    # insert for 1st request 
    insert_into(array_values,target_cur,table_to_insert)
    first_request_time = time.time()
    res = ("Done in %s seconds!" %(first_request_time- start_time))
    #target_connection commit
    target_connection.commit()
    print("commit ok. All data loaded successfully")
    return res

def launch_UpdData_constraint_tables(table_to_truncate,request,table_to_insert):
    start_time = time.time()
    #connection to city_context
    cur = connection.cursor()
    #connection to verif_shema
    target_cur = target_connection.cursor()
    #delete all table content
    try:
        target_cur.execute("TRUNCATE {0}.{1}" .format(model_params.MODEL_BDD_PARAMS['verif_quality_schema'],table_to_truncate))
        target_connection.commit() 
    except Exception as e:
        print ("erreur :" + str(e)) 
    #execute 1st request
    array_values = exec_request(cur,request)
    # insert for 1st request 
    insert_into_constraint_tables(array_values,target_cur,table_to_insert)
    first_request_time = time.time()
    res = ("Done in %s seconds!" %(first_request_time- start_time))
    #target_connection commit
    target_connection.commit()
    print("commit ok. All data loaded successfully")
    return res        

def launch_UpdData_stat(table_to_truncate,requests_list,table_to_insert):
    start_time = time.time()
    #connection to city_context
    cur = connection.cursor()
    #connection to verif_shema
    target_cur = target_connection.cursor()
    #delete all table content
    try:
        target_cur.execute("truncate {0}.count_statistics" .format(model_params.MODEL_BDD_PARAMS['verif_quality_schema']))
        target_connection.commit()     
    except Exception as e:
        print ("erreur :" + str(e)) 
    #execute household request
    arrays_list= []
    for i in requests_list:
        array_values = exec_request(cur,i)
        arrays_list.append(array_values)
        print(arrays_list)
    res_values = np.vstack(arrays_list)
    #insert household request
    insert_into_statistics_table(res_values,target_cur,model_params.MODEL_CONFIG_PARAMS['Requests_params']['Request_insert_into_count_statistics'])
    seven_request_time = time.time()
    res = ("Statistics Request done in %s seconds!" %(seven_request_time - start_time))
    #target_connection commit
    target_connection.commit()
    print("commit ok. All data loaded successfully")
    return res   