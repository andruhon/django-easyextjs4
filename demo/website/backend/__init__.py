# THIS SOFTWARE IS PROVIDED ''AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO CONTRIBUTORS BE LIABLE FOR ANY 
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY 
# OF SUCH DAMAGE.

from datetime import datetime
from EasyExtJS4 import Ext

@Ext.Class(pNameSpace = 'DemoEasyExtJS4')
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