// THIS SOFTWARE IS PROVIDED ''AS IS'' AND ANY EXPRESS OR IMPLIED
// WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
// FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO CONTRIBUTORS BE LIABLE FOR ANY 
// DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
// BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
// PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
// WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY 
// OF SUCH DAMAGE.

Ext.Loader.setConfig({enabled:true});
Ext.Loader.setPath('DemoEasyExtJS4','');

Ext.require(['DemoEasyExtJS4.view.Compute']);

Ext.application({
    name: 'EasyExtJS4 - Demo',
    launch: function() {
    	
		// Create form instance
		Ext.create('DemoEasyExtJS4.view.Compute');

		// Event			
		lOnEvent1Cpt = 1;

		Ext.direct.Manager.on('DemoEasyExtJS4.Compute.Event', function(event){
			var lMsg = 'Event: [' + lOnEvent1Cpt + '] ' + event.data,
			    lEventMsg = Ext.getCmp('idEvent'); 
            	Ext.log(lMsg);
			lEventMsg.setText(lMsg);
			lOnEvent1Cpt++;
		});

		// Display a message box if an exception on the server occur
		Ext.direct.Manager.on('exception', function(e) {
					if (e == null || e.code == 'xhr') return;
					if (e.data.Type == 'event'){
						lPoll = Ext.direct.Manager.getProvider(e.data.Id);
						lPoll.disconnect();
					}
					Ext.log({level: 'error', msg:'Exception: ' + e.message});
					Ext.Msg.show({
					           title:'Exception',
					           msg: e.message,
					           buttons: Ext.Msg.OK,
					           icon: Ext.Msg.ERROR
					    });
				});

	    }
});