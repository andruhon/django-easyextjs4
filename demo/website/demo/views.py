# THIS SOFTWARE IS PROVIDED ''AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO CONTRIBUTORS BE LIABLE FOR ANY 
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY 
# OF SUCH DAMAGE.

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
