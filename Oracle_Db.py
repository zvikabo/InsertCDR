import cx_Oracle,os
import logging

def connect_to_oracle(cfg_params):
    username = (cfg_params.get('database')).get('userid')
    password = (cfg_params.get('database')).get('password')
    hostname = (cfg_params.get('database')).get('hostid')
    port = (cfg_params.get('database')).get('port')
    db_dict = {}

    try:
        con = cx_Oracle.connect(username + '/' + password + '@' + hostname+'/gcti')
        db_dict = [con, 'Success to connect to db']
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        db_dict = ["", error.message]
    return db_dict

def oracle_execute(con, cfg_params, cdr_array, sql_stmt):
    inputsize = (cfg_params.get('sql_param')).get('inputsize')
    cur = con.cursor()
    cur.bindarraysize = len(cdr_array)

    try:
        cur.executemany(sql_stmt, cdr_array)
        con.commit()
        return_status = 'success to execute sql'
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        return_status = error.message

    cur.close()
    return return_status

def oracle_callproc(con,cdr_array):

    cur = con.cursor()

    try:
        cur.callproc('PACKAGE pck_sbc_cdr.P_INSERT_CDRS',cdr_array)
        return_status = 'success to execute sql'
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        return_status = error.message

    cur.close()
    return return_status

def oracle_disconnect(con):
    con.close()



