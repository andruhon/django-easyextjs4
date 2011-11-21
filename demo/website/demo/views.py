# For the licence see the file : LICENCE.txt

import os.path
from EasyExtJS4 import Ext
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from website import settings

@csrf_exempt
def easyextjs4(pRequest):
    
    try:
        lRet = Ext.Request(pRequest = pRequest, pRootProject = os.path.join(settings.ROOT_PATH,'app'), pRootUrl = '/easyextjs4/', pIndex = 'index.html' )
    except:# Exception as lException:
        lRet = HttpResponse(status = 400, content = '<h1>HTTP 400 - Bad Request</h1>The request cannot be fulfilled due to bad syntax.') 
        
    return lRet
