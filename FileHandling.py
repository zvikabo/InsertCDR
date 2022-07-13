import glob,  os ,time,operator, shutil,errno,configparser
import logging


def add_file_extention_1(cfg_params):
    """ The SBC ftp the files  with no extension
        this function add extension .txt to files in specific folder
    """
    filelist=[]
    cdrpath=(cfg_params.get('cdr_files')).get('path')
    cdr_prefix=(cfg_params.get('cdr_files')).get('cdr_prefix')

    try:

        for filename in glob.iglob(os.path.join(cdrpath ,cdr_prefix +'*')):
            
            if not filename.split('.')[:-1]:
                temp_file_name=filename.split('.')
                os.rename(temp_file_name[0],temp_file_name[0] +'.txt')
                
            filelist.append(filename)
            

    except:
        pass
    return (filelist)

def get_cdr_data(cdrfile,cdr_att,cfg_params):
    """
    This function get the pointer to the cdr file to read
    The content of the file store as a list and return to main function.
    
    """
    myLogger = logging.getLogger(__name__)
    cdr_array = []
    

    try:
        f = open(cdrfile, 'r')
        file_content = f.read().splitlines()
        f.close()


        for i in range(len(file_content)):
            if(file_content)[i][0] == cdr_att:
                cdr_array.append((((file_content)[i]).replace('"', '')).split(','))

        myLogger.info('--------------------------version :      ',cdr_array[0][117])

        if (cdr_array.__len__()!=0):
            tmp_array=[]
            tmp_row=[]
            for j in range (cdr_array.__len__()):
                myLogger.info(cdr_array[j])
                tmp_row=cdr_array[j][:178]+cdr_array[j][194:]
                tmp_array.append(tmp_row)
               
            
            myLogger.info('cdr array size   :   % s  rows ' % cdr_array.__len__())
            myLogger.info(cdr_array)
            
        return tmp_array
    except:
        return None

def get_cdr_data_1(cdrfile,cdr_att,cfg_params):
    
    myLogger = logging.getLogger(__name__)
    cdr_array = []
    

    try:
        f = open(cdrfile, 'r')
        file_content = f.read().splitlines()
        f.close()


        for i in range(len(file_content)):
            if(file_content)[i][0] == cdr_att:
                cdr_array.append((((file_content)[i]).replace('"', '')).split(','))

                      
            
            myLogger.info('cdr array size   :   % s  rows ' % cdr_array.__len__())
            myLogger.info(cdr_array)
            
        return cdr_array



    except:

        return None



def rename_file(filename,cfg_params,status ):
    """ this function add prefix to a file name according to the status of the process
    ( for example err_cdrxxxxx.txt or old_cdrxxxx.txt)
    """
    myLogger = logging.getLogger(__name__)
    cdrpath = (cfg_params.get('cdr_files')).get('path')
    
    if status=='processed_with_error':
        prefix= (cfg_params.get('cdr_files')).get('err_file_prefix')
        sofix = (cfg_params.get('cdr_files')).get('err_file_sofix')
    elif (status=='processed')|(status == 'proceessed_no_cdr_found'):
        prefix =(cfg_params.get('cdr_files')).get('his_file_prefix')
        sofix  =(cfg_params.get('cdr_files')).get('his_file_sofix')
    else :
        prefix =(cfg_params.get('cdr_files')).get('cdr_prefix')
        sofix  =(cfg_params.get('cdr_files')).get('cdr_extention')


    f_name = filename.split('.')
    new_f_name=cdrpath + '/' + os.sep +prefix +'_' + (f_name[0].split('/'))[-1] +'.'+ sofix
    
    try:
        #os.rename('/SBC_CTILOG/test/cdr201807281714.txt', '/SBC_CTILOG/test/zzz_cdr201807281714.txt')
        os.rename(filename,new_f_name)
        myLogger.debug( 'rename file %s : to : %s ',filename, new_f_name )
    except OSError as e:
        myLogger.info('Rename file error  :   % s  ' , filename  )
        exit()

    return new_f_name

def move_file_to_his(cfg_params,cdrfile):
    """
    This function remove to history path each file in cdrs directory with a specific prefix and sofix
    for example : C:\Temp\CDR\old_cdr201704031227.txt will be removed to C:\Temp\CDR\Old\old_cdr201704031227.txt
    if the history directory is not exir this function created it
    """
    myLogger = logging.getLogger(__name__)

    cdr_path =      (cfg_params.get('cdr_files')).get('path')
    his_prefix =    (cfg_params.get('cdr_files')).get('his_file_prefix')
    his_sofix =     (cfg_params.get('cdr_files')).get('his_file_sofix')
    root_his_path = (cfg_params.get('cdr_files')).get('root_his_file_path')
    cdr_prefix=     (cfg_params.get('cdr_files')).get('cdr_prefix')

    f_cdr = cdr_path + '/' + his_prefix + '*.' + his_sofix
    files = glob.glob(f_cdr)

    for old_f in files :

        history_directory = (((old_f.split(his_prefix + '_' + cdr_prefix))[-1]).split('/')[-1]).split('.')[-2][0:6]
        history_path= root_his_path + '/' +history_directory

        if not os.path.exists(history_path):
            try:
                os.mkdir(history_path)
                myLogger.info('created new directory  :   % s  y' % history_directory)
            except:
                err = os.error
                myLogger.info('could not create new directory   % s  error :  %s' % history_path % err )
                pass

        try:
            #print(old_f,        history_path)
            #print(old_f.split('//')[-1])
            shutil.move(old_f, history_path+ os.sep +old_f.split('/')[-1])
            myLogger.info('moving file   :   % s  to history' % old_f)
        except : pass

    return None

def get_file_size(cdr_file):
    myLogger = logging.getLogger(__name__)

    try:
        filesize= (os.path.getsize(cdr_file))/1024
        file_size = [filesize, ""]
        myLogger.info('filesize is  :   % s  KB' % filesize )

    except:
        err=os.error
        file_size=["",err]

    return file_size

def delete_file(file_name):
    myLogger = logging.getLogger(__name__)

    try:
        os.remove(file_name)
        C

    except:
        pass
    return None


