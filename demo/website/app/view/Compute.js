// THIS SOFTWARE IS PROVIDED ''AS IS'' AND ANY EXPRESS OR IMPLIED
// WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
// FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO CONTRIBUTORS BE LIABLE FOR ANY 
// DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
// BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
// PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
// WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY 
// OF SUCH DAMAGE.

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