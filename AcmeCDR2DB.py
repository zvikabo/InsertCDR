#!/usr/bin/python3

import os,glob
import Alerts_Reporting
import FileHandling
import Oracle_Db
import Initialization as Init
import fcntl
import sys

def lock(filename):
    lock_file = open(filename, 'w')
    try:
        fcntl.lockf(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        return False
    return True

lock_filename = '/usr/local/scripts/AcmeCDR2DB/AcmeCDR2DB-locking.lock'
locked = lock(lock_filename)

def main():
    p_cfgfile = os.getcwd() + '/AcmeCDR2DB.cfg'
    cfg_file = Init.cfgFile(p_cfgfile)
    cfg_params = cfg_file.get_cfg_data()
    PrvLogger = Init.MyLogger('/GCTI_Log/AcmeCDR2DB/AcmeCDR2DB.log',int(cfg_params.get('Log_File').get('maxbytes')), int(cfg_params.get('Log_File').get('backupcount')))
    myLogger = PrvLogger.getLogger()
    
    if not locked:
        myLogger.info('Cannot lock: ' + lock_filename)
        sys.exit(1)
    myLogger.info('Locked! Running code...')
    
    F_List=FileHandling.add_file_extention_1(cfg_params)
    myLogger.info(F_List)

    if F_List :
        con = Oracle_Db.connect_to_oracle (cfg_params)
        for cdrfile in glob.iglob (os.path.join (cfg_params.get('cdr_files').get('path'), 'cdr*.*')):
            myLogger.info((cdrfile))
            if cdrfile == None:
                myLogger.info('There is no file to run - finish running')
            else:
                filesize = FileHandling.get_file_size(cdrfile)
                if filesize[0] != 0:
                    myLogger.info('start running  % s ' % cdrfile)
                    cdr_types = ((cfg_params.get('sql_type')).get('cdr_type'))
                    for cdr_type in cdr_types:
                        sql_stmt = {'1': 'sql_start', '2': 'sql_stop', '3': 'sql_intrim'}
                        sql = sql_stmt.get(cdr_type)
                        sql_query = (cfg_params.get('sql_type')).get(sql)
                        cdr_array = FileHandling.get_cdr_data(cdrfile, cdr_type, cfg_params)
                        
                        if cdr_array == None:
                            status = 'proceessed_no_cdr_found'
                            myLogger.info('No_CDRs found in %s' % cdrfile)
                        else:
                           if con[1] != 'Success to connect to db':
                                myLogger.critical('Db error :   % s ' % con[1])
                                status = 'not_processed'
                                prepdata = Alerts_Reporting.PostRequest('Can not connect to DB', 'MAJOR', 'cx_Oracle','connect', '', '', '', '', '')
                                payload = prepdata.create_json_data(cfg_params)
                                retun_code = prepdata.call_rest(payload, cfg_params)
                                myLogger.info('Alerts Server error :   % s ' % retun_code)
                           else:
                                sql_execute_status = Oracle_Db.oracle_execute(con[0], cfg_params, cdr_array, sql_query)
                                

                                if sql_execute_status != 'success to execute sql':
                                    myLogger.critical('Db error :   % s ' % sql_execute_status)
                                    status = 'processed_with_error'
                                else:
                                    status = 'processed'
                                    myLogger.info('End Running')

                        FileHandling.rename_file(cdrfile, cfg_params, status)
                        myLogger.info('Rename file  :   % s ' % cdrfile)
                        FileHandling.move_file_to_his(cfg_params, cdrfile)
                        myLogger.info('Move file  :   % s  to history' % cdrfile)

                else:
                    FileHandling.delete_file(cdrfile)
                    myLogger.info('Deleted 0 size file  :   % s ' % cdrfile)

        Oracle_Db.oracle_disconnect (con[0])

    else:
        myLogger.info('No files to Run')
    sys.exit(0)

if __name__ == '__main__': main()
