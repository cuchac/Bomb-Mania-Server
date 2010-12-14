'''
Created on Nov 15, 2010

@author: root
'''
from xmlrpc.client import ServerProxy
from bm import settings_client
from django.contrib.auth.models import User
from collections import OrderedDict
from django.core.exceptions import ObjectDoesNotExist

class RPCQueryObject(OrderedDict):
    DoesNotExist = ObjectDoesNotExist
    
    def __init__(self, *args, **kwargs):
        ret = super(RPCQueryObject, self).__init__(*args, **kwargs)
        if "id" in self:
            self.id = self["id"]
            self.pk = self["id"]
        self._meta = type("Meta", (object,), {'app_label':'', 'object_name':'', 'pk':type("pk", (object,), {'name':'id'})()})()
        return ret
    
    def __str__(self):
        if "name" in self:
            return self["name"]
        else:
            return str(self["id"])
    


class RPCQuerySet(object):
    '''
    XML-RPC QuerySet-like object
    '''
    
    rpc = ServerProxy(settings_client.RPC_SERVER, verbose = False, allow_none = True, use_datetime = True)


    def __init__(self, name, id = None, auth = None, request = None, params = []):
        '''
        Construct
        
        @param name: name of data to get
        @param id: id of particular record. If empty, fetch list of records
        @param auth: (user, password) tuple if request needs authentication
        '''

        self.name = name
        self.auth = auth
        self.id = id
        self.params = params
        
        if request:
            self.auth = (request.session["username"], request.session["password"])
        
        self.data = None
        
        self.model = RPCQueryObject()
        
    def _clone(self):
        return self
    
    def __iter__(self):
        if self.data is None:
            self.fetchData()
        return self._result_iter()
    
    def _result_iter(self):
        for item in self.data:
            yield item
            
    def __getitem__(self, k):
        if self.data is None:
            self.fetchData()
        return self.data.__getitem__(k)
    
    def fetchData(self):
        if self.id is not None:
            method = "get{0}Detail".format(self.name)
        else:
            method = "list{0}s".format(self.name)
            
        self.sendRequest(method)
            
    def sendRequest(self, method, *additional_params):
            
        if hasattr(self.rpc, method):
            method = getattr(self.rpc, method)
        else:
            raise Exception("Cannot find method: {0}".format(method))
        
        params = []
        if self.auth:
            params.append(self.auth[0])
            params.append(self.auth[1])
            
        if self.id:
            params.append(self.id)
            
        params += self.params
        params += additional_params
        
        self.data = method(*params)
        
        if self.id is not None:
            self.data = [self.data]
            
    def filter(self, pk):
        self.id = pk
        return self
        
    def get(self, pk = None):
        if self.data is None:
            self.fetchData()
        if pk:
            for item in self.data:
                if item["id"] == pk:
                    return RPCQueryObject(item)
            raise Exception("Item with pk:{0} not found".format(pk))
        return RPCQueryObject(self.data[0])
    
    def all(self):
        if self.data is None:
            self.fetchData()
        return [RPCQueryObject(item) for item in self.data]

class RPCAuthUser(User):
    def __init__(self, data):
        for key,value in data.items():
            setattr(self, key, value)
            
    is_active = True
    
    def is_authenticated(self):
        return True
        
    def save(self, *args, **kwargs):
        pass

class RPCAuthBackend:
    """
    Authenticate against the RPC
    """

    def authenticate(self, username=None, password=None):
        try:
            rpc = RPCQuerySet("User", id = 0, auth = (username,password,))
            user = RPCAuthUser(list(rpc)[0])
            user.password = password
            return user
        except:
            raise
            return None

    def get_user(self, user_id):
        try:
            rpc = RPCQuerySet("Player", id = user_id)
            return RPCAuthUser(list(rpc)[0])
        except:
            raise
            return None