# For the licence see the file : LICENCE.txt

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