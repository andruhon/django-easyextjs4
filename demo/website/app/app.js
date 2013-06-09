// For the licence see the file : LICENCE.txt

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

		Ext.direct.Manager.on('DemoEasyExtJS4.Compute.Event', function(pEvent){
			var lMsg = 'Event: [' + lOnEvent1Cpt + '] ' + pEvent.data,
			    lEventMsg = Ext.getCmp('idEvent'); 
	            	Ext.log(lMsg);
			lEventMsg.setText(lMsg);
			lOnEvent1Cpt++;
		});

		// Display a message box if an exception on the server occur
		Ext.direct.Manager.on('exception', function(pException) {
			if (pException == null || pException.code == 'xhr') return;
			if (pException.data.Type == 'event'){
				lPoll = Ext.direct.Manager.getProvider(pException.data.Id);
				lPoll.disconnect();
			}
			Ext.log({level: 'error', msg:'Exception: ' + pException.message});
			Ext.Msg.show({
			           title:'Exception',
			           msg: pException.message,
			           buttons: Ext.Msg.OK,
			           icon: Ext.Msg.ERROR
			});
		});

	}
});