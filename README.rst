==========
EasyExtJS4
==========

Ext JS 4 it's powerfull javascript framework very insteresting if you want to develop professional web interface. 
Ext JS 4 provide a very powerfull mechanism to communicate with the backend: Ext Direct. 
With Ext Direct you can export your API of your application. 
EasyExtJS4 is a python package. It will manage for you all the communication with ExtJS. Make available your 
classes and methods is extremely simplified as you'll see.

------------------
Install EasyExtJS4
------------------
 
Execute these commands::
   $ cd package
   $ python setup.py install

---------------------------------------
Make available your classes and methods
---------------------------------------

Backend class
=============

To export a python class::

  from EasyExtJS4 import Ext

  @Ext.Class(pNameSpace = 'DemoEasyExtJS4', pUrlApis = 'api.js')
  class Compute(object):
    
    @staticmethod
    @Ext.StaticMethod()
    def Execute(pVal1, pOp, pVal2):
        if pOp == 'plus':
            lRet = pVal1 + pVal2
        elif pOp == 'minus':
            lRet = pVal1 - pVal2
        elif pOp == 'div':
            lRet = pVal1 / pVal2
        elif pOp == 'mul':
            lRet = pVal1 * pVal2
            
        return lRet
    
    @staticmethod
    @Ext.StaticEvent()
    def Event():
        lRet = "%s" % (datetime.utcnow())
        return lRet

With just 3 declarations **Ext.Class**, **Ext.StaticMethod** and **Ext.StaticEvent** your class will exported to Ext JS. 
The Ext JS wrapper will generate and return to '**api.js**'.

Django configuration
====================

Django view
-----------

On your file **view.py** declare a method like this one::

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

Django URL
----------

Associate this view with an url on **urls.py** like this::

  from django.conf.urls.defaults import patterns, url #, include
  from website.demo.views import easyextjs4

  urlpatterns = patterns('',
    url(r'^easyextjs4/', easyextjs4)
  )

Ext JS configuration
====================

Load wrapper
------------

To access to your python class add this line on your **index.html**::

  <script type="text/javascript" src="api.js"></script>

Call your python class
----------------------

You can call a method of your python class like this::

  handler: function(){
    ....
                            
    DemoEasyExtJS4.Compute.Execute(lVal1,lRecord.raw.exec,lVal2, function(pResult){
        lResult.setValue(pResult);
    })    
 
On this example '**DemoEasyExtJ4**' it's the name space you declare for your class, '**Compute**' it's the class and 
'**Execute**' it's a method of your class

--------------------
Run the demo project
--------------------

To execute the demo project you must have the following packages installed:
 - Django 1.3
 - EasyExtJS4 1.0

To start the demo project execute this command::

	$ python demo/website/manage.py runserver --noreload 


And finally open your browser and enter this URL::
	http://127.0.0.1:8000/easyextjs4/

Tested with python 2.7.2

