# For the licence see the file : LICENCE.txt
# this is simplified modification of https://github.com/TofPlay/django-easyextjs4
from datetime import datetime
import os, sys, functools, inspect, re, json, mimetypes
import pdb
from string import Template
from urlparse import urlparse

from django.http import HttpResponse


# TODO define global config rather than use bunch of variables to pass into
ACTION_SUFFIX = "RemoteProcedures"

__all__ = ['Ext']

# Force datetime to be compatible with Json format
ExtJsonHandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else None

class ExtJSError(Exception):

    def __init__(self, pMessage):
        self.__value = pMessage

    def __str__(self):
        return repr(self.__value)

class Ext(object):

    __URLSAPI = dict()  # List of *.js file API. Each URL point to a list of class.
    __URLSRPC = dict()  # URL for RPC. Each URL point to a list of class.
    __METHODS = dict()  # Temporary used to build internal structur for RPC
    
    __badRequest = HttpResponse(status=400, content='<h1>HTTP 400 - Bad Request</h1>The request cannot be fulfilled due to bad syntax.');

    class __Instance(object):
        pass

    class Json(object):

        @staticmethod
        def Load(pJson):
            lRet = json.loads(pJson)
            return lRet

        @staticmethod
        def Dumps(pObj):
            lRet = json.dumps(pObj, default=ExtJsonHandler)
            return lRet

    @staticmethod
    def Class(pUrlApis=None, pUrl=None, pId=None, pTimeOut=None, pNameSpace=None):

        if pId is not None and not isinstance(pId, str):
            raise ExtJSError('pId must be a string')

        if pNameSpace is not None and not isinstance(pNameSpace, str):
            raise ExtJSError('pNameSpace must be a string')

        if pTimeOut is not None and not isinstance(pTimeOut, int):
            raise ExtJSError('pTimeOut must be an integer')

        if pUrl is not None and not isinstance(pUrl, str):
            raise ExtJSError('pUrl must be a string')

        if pUrlApis is not None and not isinstance(pUrlApis, str):
            raise ExtJSError('pUrlApis must be a string')

        if pUrlApis is None:
            pUrlApis = 'api.js'

        lExt = Ext.__Instance()

        lExt.UrlApis = pUrlApis
        lExt.Url = pUrl
        lExt.Id = pId
        lExt.TimeOut = pTimeOut
        lExt.NameSpace = pNameSpace

        def decorator(pClass):

            if hasattr(pClass, '__ExtJS'):
                raise ExtJSError('Class %s already register for ExtJS' % pClass.__name__)

            # Store ExtJS informations on the class
            pClass.__ExtJS = lExt

            # Valid and store Javascript API
            if lExt.UrlApis not in Ext.__URLSAPI:
                Ext.__URLSAPI[lExt.UrlApis] = list()
            else:
                lFirstClass = Ext.__URLSAPI[lExt.UrlApis][0]
                lExtFirst = lFirstClass.__ExtJS
                if lExt.NameSpace is None:
                    # The first class has define a name space it will spread to other classes that have the same UrlApis
                    lExt.NameSpace = lExtFirst.NameSpace
                else:
                    # For an UrlApis we must define the same name space
                    if lExt.NameSpace != lExtFirst.NameSpace:
                        raise ExtJSError('Class "%s": A same javascript API ("%s") can not be define with two differents name space.' % (pClass.__name__, lExt.UrlApis))

            if lExt.Url is not None:
                lUrl = lExt.Url
            else:
                lUrl = 'Default'

                if lExt.NameSpace is not None:
                    lUrl = lExt.NameSpace

            # lExt.Url = 'Rpc' + lUrl
            # Andr: removing Rpc prefix from URL for compatibility with existing Systemfox JS api
            lExt.Url = lUrl

            if lExt.Url not in Ext.__URLSRPC:
                Ext.__URLSRPC[lExt.Url] = dict()

            Ext.__URLSRPC[lExt.Url][pClass.__name__] = pClass

            if pClass not in Ext.__URLSAPI[lExt.UrlApis]:
                Ext.__URLSAPI[lExt.UrlApis].append(pClass)

            # Register methods
            lExt.StaticMethods = Ext.__METHODS

            Ext.__METHODS = dict()

            @functools.wraps(pClass)
            def wrapper(*pArgs, **pKwargs):
                lNewObj = pClass(*pArgs, **pKwargs)
                return lNewObj

            return wrapper

        return decorator

    @staticmethod
    def StaticMethod(pNameParams=False, pTypeParams=False):

        if not isinstance(pNameParams, bool):
            raise ExtJSError('pNameParams must be a bool. True method using naming parameters, False list of parameters')

        if not isinstance(pTypeParams, bool):
            raise ExtJSError('pTypeParams must be a bool. True method support type parameters, False type is not check')

        if sys.version_info < (3, 0) and pTypeParams == True:
            raise ExtJSError('Type for parameters not supported for Python %s. Must be Python 3.x' % ".".join(str(lVal) for lVal in sys.version_info))
        else:
            if pNameParams == False and pTypeParams == True:
                raise ExtJSError('Type parameters can be activated if named parameters is also activated')

        lMethodInfo = Ext.__Instance()
        lMethodInfo.NameParams = pNameParams
        lMethodInfo.TypeParams = pTypeParams

        def decorator(pMethod):

            if type(pMethod) == staticmethod:
                raise ExtJSError('You must declare @staticmethod before @Ext.StaticMethod')

            lArgs = inspect.getargspec(pMethod)
            lParams = list(lArgs.args)

            if 'pRequest' not in lArgs.args:
                raise ExtJSError('You must declare a parameter pRequest')
            else:
                # Remove pRequest will be transmit automaticaly by the method Request
                if lParams != []:
                    # Check if pRequest is the first parameter
                    if lParams.index('pRequest') != 0:
                        raise ExtJSError('pRequest must be the first parameter')
                    lParams = [lVal for lVal in lParams if lVal != 'pRequest']

            lMethodInfo.Name = pMethod.__name__
            lMethodInfo.Args = lParams
            lMethodInfo.VarArgs = lArgs.varargs
            lMethodInfo.Keywords = lArgs.keywords
            lMethodInfo.Defaults = lArgs.defaults
            lMethodInfo.Call = pMethod

            Ext.__METHODS[pMethod.__name__] = lMethodInfo

            @functools.wraps(pMethod)
            def wrapper(*pArgs, **pKwargs):
                lRet = pMethod(*pArgs, **pKwargs)
                return lRet

            return wrapper

        return decorator

    @staticmethod
    def Request(pRequest, pRootProject=None, pRootUrl=None, pIndex='index.html', pAlias=None):
        lRet = Ext.__badRequest;

        # Valid the url.
        lPath = pRequest.path_info
        lMatch = re.match('^/[0-9a-zA-Z\.\/\-\_]*$', lPath)

        if lMatch is None:
            raise ExtJSError('You have some invalid characters on the Url: "%s"' % pRootUrl)

        if pRootUrl is not None:
            # Remove http://<host name>:<port>/ from pRootUrl
            pRootUrl = urlparse(pRootUrl).path
            # If the root for the url is specify check if the Url begin with this path

            if lPath.find(pRootUrl) != 0:
                raise ExtJSError('Invalid root for the Url: "%s"' % pRootUrl)
            # Remove url root from the path
            lPath = lPath[len(pRootUrl):]
        else:
            # If url root is not specify doesn't validate it
            pRootUrl = ''

        # Detect if the URL it's to return javascript wrapper
        lUrlApis = re.search('^([\w\/-]*\.js)$', lPath)

        if lUrlApis is not None:
            lRet = Ext.apiRequest(lPath,lUrlApis=lUrlApis)
        else:
            # Detect if the URL it's a RPC or a Poll request
            lUrlRPCsorPolls = re.search('^([\w\/-]*)$', lPath)

            if lUrlRPCsorPolls is not None:
                lUrl = lUrlRPCsorPolls.group(1)

                if lUrl in Ext.__URLSRPC:
                    lRet = Ext.remoteProcedureRequest(lUrl, pRequest=pRequest)
                    
        if lRet.status_code != 200:
            Ext.fileRequest(lPath, pRootProject=pRootProject,pIndex=pIndex)
            
        return lRet

    @staticmethod
    def apiRequest(lPath, lUrlApis=None):
        lRet = Ext.__badRequest;
        
        lUrlApi = lUrlApis.group(1)

        if lUrlApi in Ext.__URLSAPI:
            # URL found => Generate javascript wrapper
            lRemoteAPI = dict()
            for lClass in Ext.__URLSAPI[lUrlApi]:
                lExt = lClass.__ExtJS

                if lExt.Url not in lRemoteAPI:
                    # Collect all class with the same Url
                    lRemoteAPI[lExt.Url] = dict()
                    lCurrent = lRemoteAPI[lExt.Url]
                    lCurrent['url'] = lExt.Url
                    lCurrent['type'] = 'remoting'
                    if lExt.Id is not None:
                        lCurrent['id'] = lExt.Id
                    if lExt.NameSpace is not None:
                        lCurrent['namespace'] = lExt.NameSpace
                    lCurrent['actions'] = dict()
                    lAction = lCurrent['actions']

                if len(lExt.StaticMethods) > 0:
                    # Define a class as an Action with a list of functions
                    lRemoteMethods = list()
                    for lMethod in lExt.StaticMethods:
                        lMethodInfo = lExt.StaticMethods[lMethod]
                        if not lMethodInfo.NameParams:
                            lMethodExt = dict(name=lMethod, len=len(lMethodInfo.Args))
                        else:
                            # Type not supported with python 2.7 or lower.
                            if sys.version_info < (3, 0):
                                lMethodExt = dict(name=lMethod, params=lMethodInfo.Args)
                            else:
                                if not lMethodInfo.TypeParams:
                                    lMethodExt = dict(name=lMethod, params=lMethodInfo.Args)
                                else:
                                    # TODO: support this feature for python 3.x
                                    # Must return something like this :
                                    #    "params": [{
                                    #    "name": "path",
                                    #    "type": "string",
                                    #    "pos": 0
                                    #    },
                                    raise ExtJSError('Type for parameters not supported yet')
                        lRemoteMethods.append(lMethodExt)
                    # Each class is define as an 'Action'
                    lClassName = lClass.__name__
                    # remove namespace suffix from class name
                    if ACTION_SUFFIX is not None and lClassName.endswith(ACTION_SUFFIX):
                        lClassName = lClass.__name__[:-len(ACTION_SUFFIX)]
                    lAction[lClassName] = lRemoteMethods

            if len(lRemoteAPI) > 0:
                lJsonRemoteAPI = json.dumps(lRemoteAPI.values(), default=ExtJsonHandler)

                lNameSpace = lClass.__name__
                if lExt.NameSpace is not None:
                    lNameSpace = lExt.NameSpace + '.' + lNameSpace

                lContent = 'Ext.direct.Manager.addProvider(' + lJsonRemoteAPI[1:len(lJsonRemoteAPI) - 1] + ');'
                lRet = HttpResponse(content=lContent, content_type='application/javascript')
                
        return lRet;
                
    @staticmethod
    def remoteProcedureRequest(lUrl, pRequest=None):
        # URL recognized as a RPC
        lRet = Ext.__badRequest;

        # Extract data from raw post. We can not trust pRequest.POST
        lReceiveRPCs = json.loads(pRequest.body)

        # Force to be a list of dict
        if type(lReceiveRPCs) == dict:
            lReceiveRPCs = [lReceiveRPCs]

        # Extract URL
        lClassesForUrl = Ext.__URLSRPC[lUrl]

        # Initialize content
        lContent = list()

        for lReceiveRPC in lReceiveRPCs:
            # Execute each RPC request

            lRcvClass = lReceiveRPC['action'] + ACTION_SUFFIX
            lRcvMethod = lReceiveRPC['method']

            # Create name API
            lMethodName = lRcvClass + '.' + lRcvMethod

            # Prepare answer
            lAnswerRPC = dict(type='rpc', tid=lReceiveRPC['tid'], action=lRcvClass, method=lRcvMethod)

            # Prepare exception
            lExceptionData = dict(Url=lUrl, Type='rpc', Tid=lReceiveRPC['tid'], Name=lMethodName)
            lException = dict(type='exception', data=lExceptionData, message=None)

            if lRcvClass in lClassesForUrl:

                # URL for RPC founded
                lClass = lClassesForUrl[lRcvClass]
                lExt = lClass.__ExtJS

                if lRcvMethod in lExt.StaticMethods:

                    # Method founded
                    lMethod = lExt.StaticMethods[lRcvMethod]

                    # Name used for exception message
                    if lExt.NameSpace is not None:
                        lMethodName = lExt.NameSpace + '.' + lMethodName

                    # Add Id if it's define
                    if lExt.Id is not None:
                        lExceptionData['Id'] = lExt.Id

                    # Extract datas
                    lArgs = lReceiveRPC['data']

                    # Control and call method
                    if lArgs is None:
                        if len(lMethod.Args) != 0:
                            lException['message'] = '%s numbers of parameters invalid' % lMethodName
                        else:
                            try:
                                # Call method with no parameter
                                lRetMethod = lMethod.Call(pRequest=pRequest)
                                if lRetMethod is not None:
                                    lAnswerRPC['result'] = lRetMethod
                            except Exception as lErr:
                                lException['message'] = '%s: %s' % (lMethodName, str(lErr))
                    elif type(lArgs) == list:
                        if len(lArgs) > len(lMethod.Args):
                            lException['message'] = '%s numbers of parameters invalid' % lMethodName
                        else:
                            try:
                                # Call method with list of parameters
                                lArgs.insert(0, pRequest)
                                lRetMethod = lMethod.Call(*lArgs)
                                if lRetMethod is not None:
                                    lAnswerRPC['result'] = lRetMethod
                            except Exception as lErr:
                                lException['message'] = '%s: %s' % (lMethodName, str(lErr))
                    elif type(lArgs) == dict:
                        if not lMethod.NameParams:
                            lException['message'] = '%s does not support named parameters' % lMethodName
                        else:
                            if len(lArgs.keys()) > len(lMethod.Args):
                                lException['message'] = '%s numbers of parameters invalid' % lMethodName
                            else:
                                lInvalidParam = list()
                                for lParam in lArgs:
                                    if lParam not in lMethod.Args:
                                        lInvalidParam.append(lParam)
                                if len(lInvalidParam) > 0:
                                    lException['message'] = '%s: Parameters unknown -> %s' % ",".join(lInvalidParam)
                                else:
                                    try:
                                        # Call method with naming parameters
                                        lArgs['pRequest'] = pRequest
                                        lRetMethod = lMethod.Call(**lArgs)
                                        if lRetMethod is not None:
                                            lAnswerRPC['result'] = lRetMethod
                                    except Exception as lErr:
                                        lException['message'] = '%s: %s' % (lMethodName, str(lErr))
                else:
                    lException['message'] = '%s: API not found' % lMethodName

            else:
                lException['message'] = '%s: API not found' % lMethodName

            if lException['message'] is not None:
                lContent.append(lException)
            else:
                lContent.append(lAnswerRPC)

        if len(lContent) > 0:
            if len(lContent) == 1:
                lRet = HttpResponse(content=json.dumps(lContent[0], default=ExtJsonHandler), content_type='application/json')
            else:
                lRet = HttpResponse(content=json.dumps(lContent, default=ExtJsonHandler), content_type='application/json')
            return lRet

    @staticmethod
    def fileRequest(lPath,pRootProject='',pIndex=''):
        lRet = Ext.__badRequest;
        
        # The URL is not to return the API, not to execute a RPC or an event. It's just to get a file
        if pRootProject is not None:
            if not os.path.exists(pRootProject):
                raise ExtJSError('Invalid root for the project: "%s"' % pRootProject)
        else:
            # if the root project is not specify get the path of the current folder
            pRootProject = os.getcwd()

        # The path is empty try to find and load index.html (or the file specify with pIndex)
        if len(lPath) == 0:
            lPath = pIndex

        # Rebuild path to valid it
        lPath = os.path.normpath("/".join([pRootProject, lPath]))
        lFileName, lFileExt = os.path.splitext(lPath)

        # Check if the path exist and if the extension is valid
        if not os.path.exists(lPath):
            raise ExtJSError('File not found: "%s"' % lPath)
        else:
            if lFileExt not in ['.html', '.css', '.js', '.png', '.jpg', '.gif', '.json', '.xml']:
                raise ExtJSError('File extension is invalid: "%s"' % lFileExt)
            else:
                try:
                    lMime = mimetypes.types_map[lFileExt]
                except Exception as lException:
                    if isinstance(lException, KeyError) and lFileExt == '.json':
                        lMime = 'text/json'
                    else:
                        raise lException
                # TODO: Manage a chache file
                lFile = open(lPath)
                lContent = lFile.read()
                lFile.close()
                lRet = HttpResponse(content=lContent, content_type=lMime)
                
        return lRet
