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