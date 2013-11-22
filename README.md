# EasyExtJS4 [![Donate](https://github.com/TofPlay/django-easyextjs4/blob/master/PaypalDonate.png?raw=true)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=L4L34E774YLES)
Ext JS 4 it's powerfull javascript framework very insteresting if you want to develop professional web interface. 
Ext JS 4 provide a very powerfull mechanism to communicate with the backend: Ext Direct. 
With Ext Direct you can export your API of your application. 
EasyExtJS4 is a python package. It will manage for you all the communication with ExtJS (also compatible with Sencha Touch). Make available your 
classes and methods is extremely simplified as you'll see.

## Donate
You like this project. You want this project continues to evolve. You want me to publish projects even more interesting. So don't forget to click on the "Donate" button to the right of the project name.

## History

* 1.0 : First version
* 1.1 : Add support of session

## Develop with
* [Python](http://www.python.org/) 2.7.5
* [Django](https://www.djangoproject.com/) 1.5.4
* [Aptana](http://www.aptana.com/) 3.4.2

## Install EasyExtJS4

Install virtualenvwrapper:
```bash
$ pip install virtualenvwrapper
```
Create a virtual environment for EasyExtJS4:
```bash
$ mkvirtualenv easyextjs4
(easyextjs4) $ 
```
Install Django, PySqlite and EasyExtJS4:
```bash
(easyextjs4) $ pip install django pysqlite django-easyextjs4
```
Check that all installed:
```bash
(easyextjs4) $ pip freeze
Django==1.5.4
django-easyextjs4==1.1
pysqlite==2.6.3
wsgiref==0.1.2
```

## Make available your class

### Backend class

To export a python class:
  ```python
  # file: demo/website/demo/__init__.py

  from datetime import datetime
  from EasyExtJS4 import Ext

  @Ext.Class(pNameSpace = 'DemoEasyExtJS4', pSession = True)
  class Compute(object):

    @staticmethod
    @Ext.StaticMethod()
    def Execute(pSession, pVal1, pOp, pVal2):
        if pOp == 'plus':
            lRet = pVal1 + pVal2
        elif pOp == 'minus':
            lRet = pVal1 - pVal2
        elif pOp == 'div':
            lRet = pVal1 / pVal2
        elif pOp == 'mul':
            lRet = pVal1 * pVal2
      
        pSession['Execute'] = pSession.get('Execute',0) + 1   
        return lRet

    @staticmethod
    @Ext.StaticEvent()
    def Event(pSession):
        lRet = ["{}".format(datetime.utcnow()), pSession.get('Execute',0)]
        return lRet
  ```

With just 3 declarations `Ext.Class`, `Ext.StaticMethod` and `Ext.StaticEvent` your class will exported to Ext JS. 
Ext JS wrapper will generate the javascript file `api.js`.

#### Session

`pSession` is optional but when it's specify with `Ext.Class`, `Ext.StaticMethod` and `Ext.StaticEvent` it must be a method that return the current session of the user and it will be transmit to your method as the first parameter. 
If you specified `True` EasyExtJS4 will automatically extract the session object from the Django request.

* *Class session*: To manage a session for all methods and events of your class set `pSession` to `Ext.Class`.
* *Method/Event session*: To manage a session for just a few methods or events set `pSession` to `Ext.StaticMethod` and/or `Ext.StaticEvent`. `pSession` of `Ext.StaticMethod` and `Ext.StaticEvent` will overwrite `pSession` define with `Ext.Class`.

### Django configuration

#### Django view

On your file `view.py` declare a method like this one:
  ```python
  # file: demo/website/demo/views.py

  from EasyExtJS4 import Ext
  from django.views.decorators.csrf import csrf_exempt
  from django.http import HttpResponse

  from website import settings

  @csrf_exempt
  def easyextjs4(pRequest):

    try:
        lRet = Ext.Request(pRequest = pRequest, pRootProject = settings.ROOT_PATH + '/app', pRootUrl = '/', pIndex = 'app.html')
    except: #Exception as lException:
        lRet = HttpResponse(status = 400, content = '<h1>HTTP 400 - Bad Request</h1>The request cannot be fulfilled due to bad syntax.') 
    
    return lRet
  ```
`Ext.Request` will manage for you all Ext JS request like return Ext JS Wrapper for your class when you ask for `api.js`, execute RPC calls and Event calls.

#### Django URL

Associate this view with an url on `urls.py` like this:
  ```python
  # file: demo/website/urls.py

  from django.conf.urls import patterns, url #, include

  # Uncomment the next two lines to enable the admin:
  # from django.contrib import admin
  # admin.autodiscover()

  urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'website.views.home', name='home'),
    # url(r'^website/', include('website.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^.*$', 'website.demo.views.easyextjs4')
  )
  ```

### Ext JS configuration

#### Load wrapper

To access to your python class add this line on your `index.html`:
  ```html
  <script type="text/javascript" src="api.js"></script>
  ```

#### Call your python class

You can call a method of your python class like this:
  ```javascript
  /* file: demo/website/app/view/Compute.js */

  handler: function(){
                        
  DemoEasyExtJS4.Compute.Execute(lVal1,lRecord.raw.exec,lVal2, function(pResult){
      lResult.setValue(pResult);
  });    
  ``` 
On this example `DemoEasyExtJ4` it's the name space you declare for your class, `Compute` it's the class and 
`Execute` it's a method of your class

## Quick demo project

To start the demo project execute this command:
```bash
(easyextjs4) $ python demo/manage.py runserver --noreload 
```
And finally open your browser and enter this URL:

	http://127.0.0.1:8000/

You should see:

![Screenshot quick demo project](https://github.com/TofPlay/django-easyextjs4/blob/master/Screenshot.png?raw=true)

## Full demo project

For a full demo project see [Hours Tracker](https://github.com/TofPlay/HoursTracker)
