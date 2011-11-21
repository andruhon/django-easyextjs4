// For the licence see the file : LICENCE.txt

Ext.define('DemoEasyExtJS4.view.Compute', {
    extend: 'Ext.container.Viewport',

    layout: {
        align: 'center',
        pack: 'center',
        type: 'vbox'
    },

    initComponent: function() {
        var me = this;

        Ext.applyIf(me, {
            items: [
                {
                    xtype: 'form',
                    id:'idForm',
                    frame: true,
                    height: 244,
                    width: 292,
                    layout: {
                        type: 'absolute'
                    },
                    bodyPadding: 10,
                    title: 'EasyExtJS4 - Demo',
                    items: [
                        {
                            xtype: 'numberfield',
                            id: 'idVal1',
                            fieldLabel: 'Value 1',
                            value: 100
                        },
                        {
                            xtype: 'numberfield',
                            id: 'idVal2',
                            fieldLabel: 'Value 2',
                            value: 200,
                            x: 10,
                            y: 40
                        },
                        {
                            xtype: 'combobox',
                            id: 'idOp',
                            width: 150,
                            store:{
                                    fields:['display','exec'],
                                    data:[
                                      {'display':'+', 'exec':'plus'},
                                      {'display':'-', 'exec':'minus'},
                                      {'display':'/', 'exec':'div'},
                                      {'display':'*', 'exec':'mul'}
                                    ]
                            },
                            fieldLabel: 'Operator',
                            displayField:'display',
                            valueField:'exec',
                            value: '+',
                            x: 10,
                            y: 80
                        },
                        {
                            xtype: 'textfield',
                            id: 'idResult',
                            fieldLabel: 'Result',
                            x: 10,
                            y: 120
                        },
                        {
                            xtype: 'label',
                            id: 'idEvent',
                            border: '10 5 3 10',
                            height: 20,
                            width: 260,
                            text: 'Event',
                            x: 10,
                            y: 170
                        },
                        {
                            xtype: 'button',
                            text: 'Compute',
                            handler: function(){
                              var lVal1 = Ext.getCmp('idVal1').value,
                                  lVal2 = Ext.getCmp('idVal2').value,
                                  lOp = Ext.getCmp('idOp'),
                                  lResult = Ext.getCmp('idResult'),
                                  lRecord = lOp.findRecordByDisplay(lOp.rawValue);
                                  
                              DemoEasyExtJS4.Compute.Execute(lVal1,lRecord.raw.exec,lVal2, function(pResult){
                                lResult.setValue(pResult);
                              })
                            },
                            x: 200,
                            y: 80
                        }
                    ]
                }
            ]
        });

        me.callParent(arguments);
    }
});