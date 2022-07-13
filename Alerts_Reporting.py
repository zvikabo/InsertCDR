import requests
import json
import socket
import datetime
import logging

class PostRequest(object):
    """ This class send resfull request to CTI alert server ( Moshe's server) """

    def __init__(self,message,messageLevel,module,function,processID,processName,processOwner,threadName,threadID):

        self.Time = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.message = message
        self.messageLevel = messageLevel
        self.module = module
        self.function = function
        self.processID = processID
        self.processName = processName
        self.processOwner = processOwner
        self.threadName = threadName
        self.threadID = threadID
        self.machine = socket.gethostname()
        self.ip= socket.gethostbyname(socket.gethostname())

    def create_json_data(self,cfg_params):
        """This function buils the request data according to the data structure
            of the alerts server """
        payload = {
            'log':
                {
                    'Time': self.Time,
                    'message': self.message,
                    'messageLevel': self.messageLevel,
                    'module': self.module,
                    'function': self.function,
                    'processID': self.processID,
                    'processName': self.processName,
                    'processOwner': self.processOwner,
                    'threadName': self.threadName,
                    'threadID': self.threadID,
                    'machine': self.machine,
                    'ip': self.ip,
                },
            'auth':
                {
                    'user': (cfg_params.get('log_server')).get('user'),
                    'password':(cfg_params.get('log_server')).get('password'),
                }

        }
        return payload


    def call_rest(self,payload,cfg_params):
        url=(cfg_params.get('log_server')).get('url')
        headers = {'content-type': 'application/json'}
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        return r.status_code

