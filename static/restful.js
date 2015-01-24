Ext.require(['Ext.data.*', 'Ext.grid.*']);
Ext.define('ui.LoginForm',{
    extend:'Ext.form.FormPanel',
    alias: 'widget.ui.loginform',
    title:'登入表單',
    width:250,
    usernameTxt:null,
    passwordTxt:null,
    renderTarget:'container',
    usernameFL:'帳號', //username field label
    usernameFN:'username', //username field name
    passwordFL:'密碼', //password field label
    passwordFN:'password', //password field name
    fieldWidth:200,
    labelAlign:'right',
    labelWidth:50,
    submitBtnText:'送出',
    cancelBtnText:'取消',
    waitMsg:'登入中...',
    waitTitle:'資料傳送中...',
    style:'margin-left:auto;margin-right:auto',
    padding:'10px;',
    url:'',
    
    constructor:function(config){
        //Apply the configs 
        Ext.apply(this, config);
        
        if(typeof config.url == 'undefined' ||
           config.url == ''){
            throw "LoginForm must have URL to which submit the form";
        }
        
        this.initConfig(config);
        
        this.callParent([config]);
        
        return this;
    }, //eo constructor()
    
    initComponent:function(){
        
        //LoginForm Logo
        // var logo = Ext.createWidget('ui.imglabel',{
        //     id:'loginFormLogo',
        //     //img_src:Ext.fly('loginLogo').getAttribute('src'),
        //     label:'Login'
        // });
        
        //Username TextField
        var usernameTxt = { xtype:'textfield',
            id:'loginFormUsernameTxt',
            name:this.usernameFN,
            fieldLabel:this.usernameFL,
            labelWidth:this.labelWidth,
            width:this.fieldWidth,
            labelAlign:this.labelAlign,
            allowBlank: false,
            blankText:'不可空白',
            minLength: 4,
            minLengthText:'最少{0}個字元',
            msgTarget:'under'
        };
        
        //Password TextField
        var passwordTxt = { xtype:'textfield',
            id:'loginFormPasswordTxt',
            name:this.passwordFN,
            fieldLabel:this.passwordFL,
            labelWidth:this.labelWidth,
            width:this.fieldWidth,
            labelAlign:this.labelAlign,
            inputType:'password',
            allowBlank: false,
            blankText:'不可空白',
            minLength: 4,
            minLengthText:'最少{0}個字元',
            msgTarget:'under'
        };
        var tokenTxt = { xtype:'hidden',
            id:'csrfmiddlewaretoken',
            name:'csrfmiddlewaretoken',
            // fieldLabel:this.passwordFL,
            // labelWidth:this.labelWidth,
            //width:this.fieldWidth,
            // labelAlign:this.labelAlign,
            // inputType:'password',
            value:this.token,
            //allowBlank: false,
            //blankText:'不可空白',
           // minLength: 4,
            //minLengthText:'最少{0}個字元',
            //msgTarget:'under'
        };
        
        //Submit button
        var submitBtn = Ext.createWidget('button', {
            text:this.submitBtnText,
            scope:this,
            handler:this.onSubmitClickhandler,
            formBind:true
        });
        
        //Cancel button
        var cancelBtn = Ext.createWidget('button', {
            text:this.cancelBtnText,
            scope:this,
            handler:this.onCancelClickHandler
        });
        
        this.items = [ //logo, 
                       usernameTxt,
                       passwordTxt,tokenTxt];
        this.buttons =[
                       submitBtn,
                       cancelBtn
                       ];
        // this.tools = [
        //      { id:'plus' , qtip:'註冊', 
        //        scope:this, 
        //        handler:this.onSignUpClickHandler }
        // ],
        
        this.callParent();
        
        this.on('afterrender', function(){
            Ext.getCmp('loginFormUsernameTxt').focus();
        });
        
        return this;
    },//eo initComponent()
    
    //Public methods
    renderForm:function(){
        this.render(this.renderTarget);
    },//eo renderForm()
    
    onSubmitClickhandler:function(btn, evt){
        //masking the content
        this.getEl().mask('登入中','x-mask-loading');
        
        this.submit({
            scope:this,
            success:function(form, action){
                var json=action.response.responseText;
                var resO=eval("(" + json + ')');
                this.userDiv.dom.childNodes[0].data=resO.data.name;
                this.getEl().unmask('登入成功','x-mask-loading');
                this.getForm().reset();
                this.win.close();
            },//eo success()
            failure:function(form, action){
                this.getEl().unmask();
                var alertConfig = {
                    title:'錯誤',
                    //icon: Ext.window.MessageBoxWindow.ERROR,
                    buttons: Ext.Msg.OK,
                    msg:''
                };
                
                switch (action.failureType) {
                    case Ext.form.action.Action.CLIENT_INVALID:
                        alertConfig.msg = '表單值有誤';
                        break;
                    case Ext.form.action.Action.CONNECT_FAILURE:
                        alertConfig.msg = 'Ajax連線錯誤';
                        break;
                    case Ext.form.action.Action.SERVER_INVALID:
                        alertConfig.msg = '伺服器訊息：'+action.result.msg;
                }
                
                Ext.Msg.show(alertConfig);
                
            }//eo failure()
        });//eo submit()
        
    },//eo onSubmitClickhandler()
    
    onCancelClickHandler:function(btn, evt){
        evt.stopEvent();
        var form = this.getForm();
        form.reset();
    },//eo onCancelClickHandler()
    
    onSignUpClickHandler:function(){
        
        if(typeof this.signupForm == 'undefined'){
            var params = {
                url:Ext.fly('signupUrl').getAttribute('href')
            };
            this.signupForm = Ext.createWidget('ui.registerform', params);
        }
        this.signupForm.show();
    }//eo onSignUpClickHandler()
});
Ext.define('Writer.Form', {
    extend: 'Ext.form.Panel',
    alias: 'widget.writerform',

    requires: ['Ext.form.field.Text'],

    initComponent: function(){
        Ext.apply(this, {
            activeRecord: null,
            iconCls: 'icon-user',
            frame: true,
            title: 'User -- All fields are required',
            defaultType: 'textfield',
            bodyPadding: 5,
            fieldDefaults: {
                anchor: '100%',
                labelAlign: 'right'
            },
            items: [{
                fieldLabel: 'Name',
                name: 'name',
                allowBlank: false,
            },{
                fieldLabel: 'Email',
                name: 'email',
                allowBlank: false,
                vtype: 'email'
            }, {
                fieldLabel: 'First',
                name: 'first',
                allowBlank: false
            }, {
                fieldLabel: 'Last',
                name: 'last',
                allowBlank: false
            }],
            dockedItems: [{
                xtype: 'toolbar',
                dock: 'bottom',
                ui: 'footer',
                items: ['->', {
                    iconCls: 'icon-save',
                    itemId: 'save',
                    text: 'Save',
                    disabled: true,
                    scope: this,
                    handler: this.onSave
                }, {
                    iconCls: 'icon-user-add',
                    text: 'Create',
                    scope: this,
                    handler: this.onCreate
                }, {
                    iconCls: 'icon-reset',
                    text: 'Reset',
                    scope: this,
                    handler: this.onReset
                }]
            }]
        });
        this.callParent();
    },

    setActiveRecord: function(record){
        this.activeRecord = record;
        if (record) {
            this.down('#save').enable();
            this.getForm().loadRecord(record);
        } else {
            this.down('#save').disable();
            this.getForm().reset();
        }
    },

    onSave: function(){
        var active = this.activeRecord,
            form = this.getForm();

        if (!active) {
            return;
        }
        if (form.isValid()) {
            form.updateRecord(active);
            this.onReset();
        }
    },

    onCreate: function(){
        var form = this.getForm();

        if (form.isValid()) {
            this.fireEvent('create', this, form.getValues());
            form.reset();
        }

    },

    onReset: function(){
        this.setActiveRecord(null);
        this.getForm().reset();
    }
});

Ext.define('Writer.Grid', {
    extend: 'Ext.grid.Panel',
    alias: 'widget.writergrid',

    requires: [
        'Ext.grid.plugin.RowEditing',
        'Ext.form.field.Text',
        'Ext.toolbar.TextItem'
    ],

    initComponent: function(){

        this.editing = Ext.create('Ext.grid.plugin.RowEditing');//'Ext.grid.plugin.CellEditing');

        Ext.apply(this, {
            iconCls: 'icon-grid',
            frame: true,
            plugins: [this.editing],
            dockedItems: [{
                xtype: 'toolbar',
                items: [{
                    iconCls: 'icon-add',
                    text: 'Add',
                    scope: this,
                    handler: this.onAddClick
                }, {
                    iconCls: 'icon-delete',
                    text: 'Delete',
                    disabled: true,
                    itemId: 'delete',
                    scope: this,
                    handler: this.onDeleteClick
                }]
            }, {
                weight: 2,
                xtype: 'toolbar',
                dock: 'bottom',
                items: [{
                    xtype: 'tbtext',
                    text: '<b>@cfg</b>'
                }, '|', {
                    text: 'autoSync',
                    enableToggle: true,
                    pressed: true,
                    tooltip: 'When enabled, Store will execute Ajax requests as soon as a Record becomes dirty.',
                    scope: this,
                    toggleHandler: function(btn, pressed){
                        this.store.autoSync = pressed;
                    }
                }, {
                    text: 'batch',
                    enableToggle: true,
                    pressed: true,
                    tooltip: 'When enabled, Store will batch all records for each type of CRUD verb into a single Ajax request.',
                    scope: this,
                    toggleHandler: function(btn, pressed){
                        this.store.getProxy().batchActions = pressed;
                    }
                }, {
                    text: 'writeAllFields',
                    enableToggle: true,
                    pressed: false,
                    tooltip: 'When enabled, Writer will write *all* fields to the server -- not just those that changed.',
                    scope: this,
                    toggleHandler: function(btn, pressed){
                        this.store.getProxy().getWriter().writeAllFields = pressed;
                    }
                }]
            }, {
                weight: 1,
                xtype: 'toolbar',
                dock: 'bottom',
                ui: 'footer',
                items: ['->', {
                    iconCls: 'icon-save',
                    text: 'Sync',
                    scope: this,
                    handler: this.onSync
                }]
            }],
            columns: [{
                text: 'ID',
                width: 40,
                sortable: true,
                resizable: false,
                draggable: false,
                hideable: false,
                menuDisabled: true,
                dataIndex: 'id',
                renderer: function(value){
                    return Ext.isNumber(value) ? value : '&nbsp;';
                }
            }, {
                header: 'Name',
                flex: 1,
                sortable: true,
                dataIndex: 'name',
                field: {
                    type: 'textfield'
                }
            }, {
                header: 'Email',
                flex: 1,
                sortable: true,
                dataIndex: 'email',
                field: {
                    type: 'textfield'
                }
            }, {
                header: 'First',
                width: 100,
                sortable: true,
                dataIndex: 'first',
                field: {
                    type: 'textfield'
                }
            }, {
                header: 'Last',
                width: 100,
                sortable: true,
                dataIndex: 'last',
                field: {
                    type: 'textfield'
                }
            }]
        });
        this.callParent();
        this.getSelectionModel().on('selectionchange', this.onSelectChange, this);
    },
    
    onSelectChange: function(selModel, selections){
        this.down('#delete').setDisabled(selections.length === 0);
    },

    onSync: function(){
        this.store.sync();
    },

    onDeleteClick: function(){
        var selection = this.getView().getSelectionModel().getSelection()[0];
        if (selection) {
            this.store.remove(selection);
        }
    },

    onAddClick: function(){
        var rec = new Writer.Person({
            first: '',
            last: '',
            email: ''
        }), edit = this.editing;

        edit.cancelEdit();
        this.store.insert(0, rec);
        edit.startEditByPosition({
            row: 0,
            column: 1
        });
    }
});
Ext.define('Item.Form', {
    extend: 'Ext.form.Panel',
    alias: 'widget.itemform',

    requires: ['Ext.form.field.Text'],

    initComponent: function(){
        Ext.apply(this, {
            activeRecord: null,
            iconCls: 'icon-user',
            frame: true,
            title: 'Item -- All fields are required',
            defaultType: 'textfield',
            bodyPadding: 5,
            fieldDefaults: {
                anchor: '100%',
                labelAlign: 'right'
            },
            items: [{
                fieldLabel: 'Name',
                name: 'name',
                allowBlank: false,
            },{
                fieldLabel: 'Email',
                name: 'email',
                allowBlank: false,
                vtype: 'email'
            }, {
                fieldLabel: 'First',
                name: 'first',
                allowBlank: false
            }, {
                fieldLabel: 'Last',
                name: 'last',
                allowBlank: false
            }],
            dockedItems: [{
                xtype: 'toolbar',
                dock: 'bottom',
                ui: 'footer',
                items: ['->', {
                    iconCls: 'icon-save',
                    itemId: 'save',
                    text: 'Save',
                    disabled: true,
                    scope: this,
                    handler: this.onSave
                }, {
                    iconCls: 'icon-user-add',
                    text: 'Create',
                    scope: this,
                    handler: this.onCreate
                }, {
                    iconCls: 'icon-reset',
                    text: 'Reset',
                    scope: this,
                    handler: this.onReset
                }]
            }]
        });
        this.callParent();
    },

    setActiveRecord: function(record){
        this.activeRecord = record;
        if (record) {
            this.down('#save').enable();
            this.getForm().loadRecord(record);
        } else {
            this.down('#save').disable();
            this.getForm().reset();
        }
    },

    onSave: function(){
        var active = this.activeRecord,
            form = this.getForm();

        if (!active) {
            return;
        }
        if (form.isValid()) {
            form.updateRecord(active);
            this.onReset();
        }
    },

    onCreate: function(){
        var form = this.getForm();

        if (form.isValid()) {
            this.fireEvent('create', this, form.getValues());
            form.reset();
        }

    },

    onReset: function(){
        this.setActiveRecord(null);
        this.getForm().reset();
    }
});

Ext.define('Item.Grid', {
    extend: 'Ext.grid.Panel',
    alias: 'widget.itemgrid',

    requires: [
        'Ext.grid.plugin.RowEditing',
        'Ext.form.field.Text',
        'Ext.toolbar.TextItem'
    ],

    initComponent: function(){

        this.editing = Ext.create('Ext.grid.plugin.RowEditing');//'Ext.grid.plugin.CellEditing');

        Ext.apply(this, {
            bbar:this.paginTB,
            height:250,
            iconCls: 'icon-grid',
            frame: true,
            plugins: [this.editing],
            dockedItems: [{
                xtype: 'toolbar',
                items: [{
                    iconCls: 'icon-add',
                    text: 'Add',
                    scope: this,
                    handler: this.onAddClick
                }, {
                    iconCls: 'icon-delete',
                    text: 'Delete',
                    disabled: true,
                    itemId: 'delete',
                    scope: this,
                    handler: this.onDeleteClick
                }]
            }, {
                weight: 2,
                xtype: 'toolbar',
                dock: 'bottom',
                items: [
                // {
                //     xtype: 'tbtext',
                //     text: '<b>@cfg</b>'
                // }, '|', 
                {
                    text: 'autoSync',
                    enableToggle: true,
                    pressed: true,
                    tooltip: 'When enabled, Store will execute Ajax requests as soon as a Record becomes dirty.',
                    scope: this,
                    toggleHandler: function(btn, pressed){
                        this.store.autoSync = pressed;
                    }
                }, {
                    text: 'batch',
                    enableToggle: true,
                    pressed: true,
                    tooltip: 'When enabled, Store will batch all records for each type of CRUD verb into a single Ajax request.',
                    scope: this,
                    toggleHandler: function(btn, pressed){
                        this.store.getProxy().batchActions = pressed;
                    }
                }, {
                    text: 'writeAllFields',
                    enableToggle: true,
                    pressed: false,
                    tooltip: 'When enabled, Writer will write *all* fields to the server -- not just those that changed.',
                    scope: this,
                    toggleHandler: function(btn, pressed){
                        this.store.getProxy().getWriter().writeAllFields = pressed;
                    }
                }]
            }, {
                weight: 1,
                xtype: 'toolbar',
                dock: 'bottom',
                ui: 'footer',
                items: ['->', {
                    iconCls: 'icon-save',
                    text: 'Sync',
                    scope: this,
                    handler: this.onSync
                }]
            }],
            columns: [{
                    text: 'ID',
                    width: 50,
                    sortable: true,
                    dataIndex: 'id',
                }, {
                    text: '编号',
                    flex: 1,
                    sortable: true,
                    dataIndex: 'bh',
                    field: {
                        xtype: 'textfield'
                    }
                }, {
                    header: '名称',
                    width: 120,
                    sortable: true,
                    dataIndex: 'name',
                    field: {
                        xtype: 'textfield'
                    }
                }, {
                    header: '规格',
                    width: 120,
                    sortable: true,
                    dataIndex: 'guige',
                    field: {
                        xtype: 'textfield'
                    }
                }, {
                    header: '单位',
                    width: 120,
                    sortable: true,
                    dataIndex: 'danwei',
                    field: {
                        xtype: 'textfield'
                    }
                }]
        });
        this.callParent();
        this.getSelectionModel().on('selectionchange', this.onSelectChange, this);
    },
    
    onSelectChange: function(selModel, selections){
        this.down('#delete').setDisabled(selections.length === 0);
    },

    onSync: function(){
        this.store.sync();
    },

    onDeleteClick: function(){
        var selection = this.getView().getSelectionModel().getSelection()[0];
        if (selection) {
            this.store.remove(selection);
        }
    },

    onAddClick: function(){
         var rec = new Item({
            name: '',
            bh: '',
        });
        edit = this.editing;

        edit.cancelEdit();
        //this.store.insert(0, rec);
        this.store.add(rec);
        edit.startEdit(rec,0);
    }
});
Ext.define('Writer.Person', {
    extend: 'Ext.data.Model',
    fields: [{
        name: 'id',
        type: 'int',
        useNull: true
    },'name', 'email', 'first', 'last'],
    validators: {
        email: {
            type: 'length',
            min: 1
        },
        first: {
            type: 'length',
            min: 1
        },
        last: {
            type: 'length',
            min: 1
        }
    }
});
Ext.define('Item', {
    extend: 'Ext.data.Model',
    clientIdProperty: 'clientId',
    fields: [{
        name: 'id',
        type: 'int',
        useNull: true
    }, 'bh', 'name','guige','danwei'],
    validators: {
        name: {
            type: 'length',
            min: 1
        },
    }
});
Ext.define('Contact', {
    extend: 'Ext.data.Model',
    fields: [{
        name: 'id',
        type: 'int',
        useNull: true
    }
    , 'yonghu', 'yiqixinghao','yiqibh','baoxiang','shenhe',{name:'yujifahuo_date',type:"date"},'hetongbh'],
});
Ext.define('ContactItem', {
    extend: 'Ext.data.Model',
    fields: [{
        name: 'id',
        type: 'int',
        useNull: true
    }, 'contact', 'item','ct','hetongbh',"name"],
});
Ext.onReady(function(){
    var movieList = Ext.get('csrf');
    var a=movieList.dom.childNodes[0];
    var token=a.defaultValue;
    var userDiv = Ext.get('user');
    var a=userDiv.dom.childNodes[0];
    var user=a.data;
    /////////
    var load_user_edit=function(){    
        var store = Ext.create('Ext.data.Store', {
            model: 'Writer.Person',
            autoLoad: true,
            autoSync: true,
            proxy: {
                type: 'ajax',
                api: {
                    read: '/rest/app.php_users_view',
                    create: '/rest/app.php_users_create',
                    update: '/rest/app.php_users_update',
                    destroy: '/rest/app.php_users_destroy'
                },
                reader: {
                    type: 'json',
                    successProperty: 'success',
                    rootProperty: 'data',
                    messageProperty: 'message'
                },
                writer: {
                    type: 'json',
                    writeAllFields: false,
                    rootProperty: 'data'
                },
                listeners: {
                    exception: function(proxy, response, operation){
                        Ext.MessageBox.show({
                            title: 'REMOTE EXCEPTION',
                            msg: operation.getError(),
                            icon: Ext.MessageBox.ERROR,
                            buttons: Ext.Msg.OK
                        });
                    }
                }
            },
            listeners: {
                write: function(proxy, operation){
                    if (operation.action == 'destroy') {
                        main.child('#form').setActiveRecord(null);
                    }
                    //Ext.example.msg(operation.action, operation.getResultSet().message);
                }
            }
        });
        var headers={}||store.proxy.headers;
            headers["X_CSRFTOKEN"]=token;
            headers["Content-Type"]="application/json"//multipart/form-data;charset=UTF-8";
            store.proxy.headers=headers;
        var main = Ext.create('Ext.container.Container', {
            padding: '0 0 0 20',
            width: 500,
            height: Ext.themeName === 'neptune' ? 500 : 450,
            renderTo: document.body,
            layout: {
                type: 'vbox',
                align: 'stretch'
            },
            items: [{
                itemId: 'form',
                xtype: 'writerform',
                manageHeight: false,
                margin: '0 0 10 0',
                listeners: {
                    create: function(form, data){
                        store.insert(0, data);
                    }
                }
            }, {
                itemId: 'grid',
                xtype: 'writergrid',
                title: 'User List',
                flex: 1,
                store: store,
                listeners: {
                    selectionchange: function(selModel, selected) {
                        main.child('#form').setActiveRecord(selected[0] || null);
                    }
                }
            }]
        });
        return main;
    };
    /////////////////////////////////////////////////////////////////////////
    var loadContactItem=function(contact){
        var pageSize1=10;
        var contactid=contact.id;
        var store = Ext.create('Ext.data.Store', {
            pageSize:pageSize1,
            autoLoad: false,
            //autoSync: true,
            model: 'ContactItem',
            proxy: {
                type: 'rest',
                url: '/rest/contactitem/?contact='+contact.id,
                useDefaultXhrHeader: false,
                reader: {
                    type: 'json',
                    rootProperty: 'results'
                },
                writer: {
                    type: 'json'
                }
            },
            listeners: {
                write: function(store, operation){
                    var record = operation.getRecords()[0],
                        name = Ext.String.capitalize(operation.action),
                        verb;
     
                    if (name == 'Destroy') {
                        verb = 'Destroyed';
                    } else {
                        verb = name + 'd';
                    }
                }
            }
        });
        var paginTB = {
            xtype:'pagingtoolbar',
            store:store,
            pageSize:pageSize1,
            displayInfo:true
        };
        var headers={}||store.proxy.headers;
        headers["X_CSRFTOKEN"]=token;
        headers["Content-Type"]="application/json"//multipart/form-data;charset=UTF-8";
        store.proxy.headers=headers;
        var rowEditing = Ext.create('Ext.grid.plugin.RowEditing', {
            listeners: {
                beforeedit:function(rowEditing, contextrowEditing, contextrowEditing, context){
                    console.log("beforeedit");
                },
                cancelEdit: function(rowEditing, context) {
                    console.log("cancel edit");
                    if (context.record.phantom) {
                        store.remove(context.record);
                    }
                },
                validateedit:function(rowEditing, context){
                },
                edit:function(rowEditing, context){
                    store.sync();
                },
            }
        });
      
        var grid = Ext.create('Ext.grid.Panel', {
            //renderTo: "container2",
            bbar:paginTB,
            plugins: [rowEditing],
            width: 500,
            height: 330,
            frame: true,
            title: contact.hetongbh+' 合同配件',
            store: store,
            iconCls: 'icon-contact-item',
            columns: [{
                text: 'ID',
                width: 50,
                sortable: true,
                dataIndex: 'id',
            },
            {
                text: '合同id',
                flex: 1,
                dataIndex: 'contact',
                field: {
                    xtype: 'textfield'
                }
            },
            {
                text: '合同号',
                flex: 1,
                sortable: true,
                dataIndex: 'hetongbh',
                field: {
                    xtype: 'displayfield'
                }
            },{
                header: '部件id',
                width: 120,
                sortable: true,
                dataIndex: 'item',
                field: {
                    xtype: 'textfield'
                }
            },{
                header: '部件名称',
                width: 120,
                sortable: true,
                dataIndex: 'name',
                field: {
                    xtype: 'displayfield'
                }
            }, {
                header: '数量',
                width: 120,
                sortable: true,
                dataIndex: 'ct',
                field: {
                    xtype: 'textfield'
                }
            }],
            dockedItems: [{
                xtype: 'toolbar',
                items: [{
                    text: 'Add',
                    iconCls: 'icon-add',
                    handler: function(){
                        selectContactItem(contact,store);
                        // rowEditing.cancelEdit();

                        // // Create a model instance
                        // var r = Ext.create('ContactItem', {
                        //     contact: contact.id,
                        // });
                        // store.insert(0, r);
                        // rowEditing.startEdit(0,0);
                    }
                }, '-', {
                    itemId: 'delete',
                    text: 'Delete',
                    iconCls: 'icon-delete',
                    disabled: true,
                    handler: function(){
                        var selection = grid.getView().getSelectionModel().getSelection()[0];
                        if (selection) {
                                 Ext.Msg.show({
                                     message:'确实删除?',
                                     buttons: Ext.Msg.YESNO,
                                     icon: Ext.Msg.QUESTION,
                                     fn: function(btn) {
                                         if (btn === 'yes') {
                                             store.remove(selection);
                                             store.sync();
                                         } else if (btn === 'no') {
                                             console.log('No pressed');
                                         } else {
                                             console.log('Cancel pressed');
                                         } 
                                     }
                                 });
                        }
                    }
                }]
            }]
        });
        grid.getSelectionModel().on('selectionchange', function(selModel, selections){
            grid.down('#delete').setDisabled(selections.length === 0);
        });
        store.load({params:{start:0, limit:pageSize1}});
        return grid;
    };
    /////////////////////////////////////////////////////////////////////////////////////////
    var loadContact=function(){
        var store = Ext.create('Ext.data.Store', {
            autoLoad: true,
            autoSync: true,
            model: 'Contact',
            proxy: {
                type: 'rest',
                url: '/rest/contact',
                useDefaultXhrHeader: false,
                reader: {
                    type: 'json',
                    rootProperty: 'data'
                },
                writer: {
                    type: 'json'
                }
            },
            listeners: {
                write: function(store, operation){
                    var record = operation.getRecords()[0],
                        name = Ext.String.capitalize(operation.action),
                        verb;
     
                    if (name == 'Destroy') {
                        verb = 'Destroyed';
                    } else {
                        verb = name + 'd';
                    }
                    //Ext.example.msg(name, Ext.String.format("{0} user: {1}", verb, record.getId()));
                }
            }
        });
        var headers={}||store.proxy.headers;
        headers["X_CSRFTOKEN"]=token;
        headers["Content-Type"]="application/json"//multipart/form-data;charset=UTF-8";
        store.proxy.headers=headers;
        var rowEditing = Ext.create('Ext.grid.plugin.RowEditing', {
            listeners: {
                cancelEdit: function(rowEditing, context) {
                    // Canceling editing of a locally added, unsaved record: remove it
                    if (context.record.phantom) {
                        store.remove(context.record);
                    }
                }
            }
        });
      
        var grid = Ext.create('Ext.grid.Panel', {
            //renderTo: "container2",
            plugins: [rowEditing],
            width: 500,
            height: 330,
            frame: true,
            title: '合同',
            store: store,
            iconCls: 'icon-contact',
            columns: [{
                text: 'ID',
                //width: 50,
                sortable: true,
                dataIndex: 'id',
            }, {
                text: '用户',
                flex: 1,
                sortable: true,
                dataIndex: 'yonghu',
                field: {
                    xtype: 'textfield'
                }
            }, {
                header: '合同编号',
                //width: 120,
                sortable: true,
                dataIndex: 'hetongbh',
                field: {
                    xtype: 'textfield'
                }
            }, {
                header: '预计发货时间',
                //width: 120,
                sortable: true,
                dataIndex: 'yujifahuo_date',
                field: {
                    xtype: 'datefield'
                }
            }, {
                header: '包箱',
                //width: 120,
                sortable: true,
                dataIndex: 'baoxiang',
                field: {
                    xtype: 'textfield'
                }
            }],
            dockedItems: [{
                xtype: 'toolbar',
                items: [
                
                {
                    text: 'Add',
                    iconCls: 'icon-add',
                    handler: function(){
                        // empty record
                        store.insert(0, new Contact());
                        rowEditing.startEdit(0, 0);
                    }
                }, 
                '-', 
                {
                    itemId: 'delete',
                    text: 'Delete',
                    iconCls: 'icon-delete',
                    disabled: true,
                    handler: function(){
                        var selection = grid.getView().getSelectionModel().getSelection()[0];
                        if (selection) {
                                 Ext.Msg.show({
                                     //title:'确实删除?',
                                     message:'确实删除?',
                                     buttons: Ext.Msg.YESNO,
                                     icon: Ext.Msg.QUESTION,
                                     fn: function(btn) {
                                         if (btn === 'yes') {
                                             store.remove(selection);
                                         } else if (btn === 'no') {
                                             console.log('No pressed');
                                         } else {
                                             console.log('Cancel pressed');
                                         } 
                                     }
                                 });
                        }
                    }
                },
                {
                    text: 'Items',
                    iconCls: 'icon-edit',
                    handler: function(){
                        var selection = grid.getView().getSelectionModel().getSelection()[0];
                        if (selection) {
                            onContactItem(selection.data);
                        }
                    }
                }
                ]
            }]
        });
        grid.getSelectionModel().on('selectionchange', function(selModel, selections){
            grid.down('#delete').setDisabled(selections.length === 0);
        });
        
        return grid;
    };
    //////////////////////////////////////////////////////////////
    var loadItem=function(hasbutton,dest_store,contact,window){
        var pageSize1=10;

        var store = Ext.create('Ext.data.Store', {
            pageSize:pageSize1,
            autoLoad: true,
            autoSync: true,
            model: 'Item',
            proxy: {
                type: 'rest',
                url: '/rest/item',
                useDefaultXhrHeader: false,
                reader: {
                    type: 'json',
                    rootProperty: 'data'
                },
                writer: {
                    type: 'json'
                }
            },
            // listeners: {
            //     write: function(store, operation){
            //         var record = operation.getRecords()[0],
            //             name = Ext.String.capitalize(operation.action),
            //             verb;
     
            //         if (name == 'Destroy') {
            //             verb = 'Destroyed';
            //         } else {
            //             verb = name + 'd';
            //         }
            //         //Ext.example.msg(name, Ext.String.format("{0} user: {1}", verb, record.getId()));
                    
            //     }
            // }
        });
        var headers={}||store.proxy.headers;
        headers["X_CSRFTOKEN"]=token;
        headers["Content-Type"]="application/json"//multipart/form-data;charset=UTF-8";
        store.proxy.headers=headers;
        var paginTB = {
            xtype:'pagingtoolbar',
            store:store,
            pageSize:pageSize1,
            displayInfo:true
        };
        var rowEditing = Ext.create('Ext.grid.plugin.RowEditing');
        // var rowEditing = Ext.create('Ext.grid.plugin.RowEditing', {
        //     listeners: {
        //         cancelEdit: function(rowEditing, context) {
        //             // Canceling editing of a locally added, unsaved record: remove it
        //             if (context.record.phantom) {
        //                 store.remove(context.record);
        //             }
        //         }
        //     }
        // });
        var queryStore = function(){
                var targetString = Ext.getCmp('queryText1').getValue();
                var targetString2 = Ext.getCmp('queryText2').getValue();
                // if(targetString == ''){
                //     return;
                // }
                //var lastOptions = store.lastOptions;
                //lastOptions.search=targetString;
                store.load({params:{start:0, limit:pageSize1,search:targetString,search_bh:targetString2}});
            }
            var queryStore_2 = function(){
                var targetString = Ext.getCmp('queryText1_2').getValue();
                var targetString2 = Ext.getCmp('queryText2_2').getValue();
                // if(targetString == ''){
                //     return;
                // }
                //var lastOptions = store.lastOptions;
                //lastOptions.search=targetString;
                store.load({params:{start:0, limit:pageSize1,search:targetString,search_bh:targetString2}});
            }
        if(hasbutton==undefined)
        {
            var grid = Ext.create('Ext.grid.Panel', {
                //renderTo: "container2",
                bbar:paginTB,
                plugins: [rowEditing],
                width: 500,
                height: 330,
                frame: true,
                title: '部件',
                store: store,
                iconCls: 'icon-item',
                columns: [{
                    text: 'ID',
                    width: 50,
                    sortable: true,
                    dataIndex: 'id',
                }, {
                    text: '编号',
                    flex: 1,
                    sortable: true,
                    dataIndex: 'bh',
                    field: {
                        xtype: 'textfield'
                    }
                }, {
                    header: '名称',
                    width: 120,
                    sortable: true,
                    dataIndex: 'name',
                    field: {
                        xtype: 'textfield'
                    }
                }, {
                    header: '规格',
                    width: 120,
                    sortable: true,
                    dataIndex: 'guige',
                    field: {
                        xtype: 'textfield'
                    }
                }, {
                    header: '单位',
                    width: 120,
                    sortable: true,
                    dataIndex: 'danwei',
                    field: {
                        xtype: 'textfield'
                    }
                }],
                dockedItems: [{
                    xtype: 'toolbar',
                    items: [
                    { xtype:'textfield', emptyText:'請輸入名称...', width:100, id:'queryText1' },
                    { xtype:'textfield', emptyText:'請輸入编号...', width:100, id:'queryText2' },
                    { xtype:'button', text:'搜尋', handler:queryStore, scope:this },
                    {

                        text: 'Add',
                        iconCls: 'icon-add',
                        handler: function(){
                            // empty record
                            store.insert(0, new Item());
                            rowEditing.startEdit(0, 0);
                        }
                    }, '-', {
                        itemId: 'delete',
                        text: 'Delete',
                        iconCls: 'icon-delete',
                        disabled: true,
                        handler: function(){
                            var selection = grid.getView().getSelectionModel().getSelection()[0];
                            if (selection) {
                                     Ext.Msg.show({
                                         //title:'确实删除?',
                                         message:'确实删除?',
                                         buttons: Ext.Msg.YESNO,
                                         icon: Ext.Msg.QUESTION,
                                         fn: function(btn) {
                                             if (btn === 'yes') {
                                                store.remove(selection);
                                             } else if (btn === 'no') {
                                                 console.log('No pressed');
                                             } else {
                                                 console.log('Cancel pressed');
                                             } 
                                         }
                                     });
                            }
                        }
                    }]
                }]
            });
            grid.getSelectionModel().on('selectionchange', function(selModel, selections){
                grid.down('#delete').setDisabled(selections.length === 0);
            });
        }
        else
        {
            var grid = Ext.create('Ext.grid.Panel', {
                //renderTo: "container2",
                bbar:paginTB,
                plugins: [rowEditing],
                width: 500,
                height: 330,
                frame: true,
                title: '部件',
                store: store,
                iconCls: 'icon-item',
                columns: [{
                    text: 'ID',
                    width: 50,
                    sortable: true,
                    dataIndex: 'id',
                }, {
                    text: '编号',
                    flex: 1,
                    sortable: true,
                    dataIndex: 'bh',
                    field: {
                        xtype: 'textfield'
                    }
                }, {
                    header: '名称',
                    width: 120,
                    sortable: true,
                    dataIndex: 'name',
                    field: {
                        xtype: 'textfield'
                    }
                }, {
                    header: '规格',
                    width: 120,
                    sortable: true,
                    dataIndex: 'guige',
                    field: {
                        xtype: 'textfield'
                    }
                }, {
                    header: '单位',
                    width: 120,
                    sortable: true,
                    dataIndex: 'danwei',
                    field: {
                        xtype: 'textfield'
                    }
                }],
                dockedItems: [{
                    xtype: 'toolbar',
                    items: [
                    { xtype:'textfield', emptyText:'請輸入名称...', width:100, id:'queryText1_2' },
                    { xtype:'textfield', emptyText:'請輸入编号...', width:100, id:'queryText2_2' },
                    { xtype:'button', text:'搜尋', handler:queryStore_2, scope:this },
                    { xtype:'displayfield', value:"count" },
                    { xtype:'textfield', emptyText:'请输入数量...', value:"1",width:30, id:'queryText_2' }
                    ,
                    {
                        itemId: 'select',
                        text: 'select',
                        disabled: true,
                        handler: function(){
                            var selection = grid.getView().getSelectionModel().getSelection()[0];
                            if (selection) {
                                var targetString = Ext.getCmp('queryText_2').getValue();
                                var r = Ext.create('ContactItem', {
                                    contact: contact.id,
                                    item:selection.data.id,
                                    name:selection.data.name,
                                    ct:targetString
                                });
                                dest_store.add(r);
                                dest_store.sync();
                                dest_store.load();
                                window.close();
                            }
                        }
                    }
                    ]//items
                }]//dockeditems
            });
            grid.getSelectionModel().on('selectionchange', function(selModel, selections){
                grid.down('#select').setDisabled(selections.length === 0);
            });
        }
        return grid;
    };
    //loadItemNew//
    var loadItemNew=function(){
        var pageSize1=10;
        var store = Ext.create('Ext.data.Store', {
            pageSize:pageSize1,
            autoLoad: true,
            autoSync: true,
            model: 'Item',
            proxy: {
                type: 'ajax',
                api: {
                    read: '/rest/view_item2',
                    create: '/rest/create_item2',
                    update: '/rest/update_item2',
                    destroy: '/rest/destroy_item2'
                },
                reader: {
                    type: 'json',
                    successProperty: 'success',
                    rootProperty: 'data',
                    messageProperty: 'message'
                },
                writer: {
                    type: 'json',
                    writeAllFields: false,
                    rootProperty: 'data'
                },
                listeners: {
                    exception: function(proxy, response, operation){
                        Ext.MessageBox.show({
                            title: 'REMOTE EXCEPTION',
                            msg: operation.getError(),
                            icon: Ext.MessageBox.ERROR,
                            buttons: Ext.Msg.OK
                        });
                    }
                }
            },
        });
         var headers={}||store.proxy.headers;
            headers["X_CSRFTOKEN"]=token;
            headers["Content-Type"]="application/json"//multipart/form-data;charset=UTF-8";
            store.proxy.headers=headers;
        var paginTB = {
            xtype:'pagingtoolbar',
            store:store,
            pageSize:pageSize1,
            displayInfo:true
        };
        var main = Ext.create('Ext.container.Container', {
            padding: '0 0 0 20',
            width: 500,
            height: 380,
            renderTo: document.body,
            layout: {
                type: 'vbox',
                align: 'stretch'
            },
            items: [
            // {
            //     itemId: 'form',
            //     xtype: 'itemform',
            //     manageHeight: false,
            //     margin: '0 0 10 0',
            //     listeners: {
            //         create: function(form, data){
            //             store.insert(0, data);
            //         }
            //     }
            // }, 
            {
                itemId: 'grid',
                xtype: 'itemgrid',
                title: 'Item List',
                flex: 1,
                store: store,
                paginTB:paginTB,
                listeners: {
                    selectionchange: function(selModel, selected) {
                        //main.child('#form').setActiveRecord(selected[0] || null);
                    }
                }
            }]
        });
        return main;
    };
    ////////////////////////////////////////////////////////////
    // var loadUser=function(){
    //     var store = Ext.create('Ext.data.Store', {
    //         autoLoad: true,
    //         autoSync: true,
    //         model: 'Person',
    //         proxy: {
    //             type: 'rest',
    //             url: '/rest/application',
    //             useDefaultXhrHeader: false,
    //             reader: {
    //                 type: 'json',
    //                 rootProperty: 'data'
    //             },
    //             writer: {
    //                 type: 'json'
    //             }
    //         },
    //         listeners: {
    //             write: function(store, operation){
    //                 var record = operation.getRecords()[0],
    //                     name = Ext.String.capitalize(operation.action),
    //                     verb;
     
    //                 if (name == 'Destroy') {
    //                     verb = 'Destroyed';
    //                 } else {
    //                     verb = name + 'd';
    //                 }
    //                 //Ext.example.msg(name, Ext.String.format("{0} user: {1}", verb, record.getId()));
                    
    //             }
    //         }
    //     });
    //     var headers={}||store.proxy.headers;
    //     headers["X_CSRFTOKEN"]=token;
    //     headers["Content-Type"]="application/json"//multipart/form-data;charset=UTF-8";
    //     store.proxy.headers=headers;
    //     var rowEditing = Ext.create('Ext.grid.plugin.RowEditing', {
    //         listeners: {
    //             cancelEdit: function(rowEditing, context) {
    //                 // Canceling editing of a locally added, unsaved record: remove it
    //                 if (context.record.phantom) {
    //                     store.remove(context.record);
    //                 }
    //             }
    //         }
    //     });
        
    //     var grid = Ext.create('Ext.grid.Panel', {
    //         //renderTo: "container2",
    //         plugins: [rowEditing],
    //         width: 500,
    //         height: 330,
    //         frame: true,
    //         title: 'Users',
    //         store: store,
    //         iconCls: 'icon-user',
    //         columns: [{
    //             text: 'ID',
    //             width: 50,
    //             sortable: true,
    //             dataIndex: 'id',
    //             renderer: function(v, meta, rec) {
    //                 return rec.phantom ? '' : v;
    //             }
    //         }, {
    //             text: 'Email',
    //             flex: 1,
    //             sortable: true,
    //             dataIndex: 'email',
    //             field: {
    //                 xtype: 'textfield'
    //             }
    //         }, {
    //             header: 'username',
    //             width: 120,
    //             sortable: true,
    //             dataIndex: 'username',
    //             field: {
    //                 xtype: 'textfield'
    //             }
    //         }],
    //         dockedItems: [{
    //             xtype: 'toolbar',
    //             items: [{
    //                 text: 'Add',
    //                 iconCls: 'icon-add',
    //                 handler: function(){
    //                     // empty record
    //                     store.insert(0, new Person());
    //                     rowEditing.startEdit(0, 0);
    //                 }
    //             }, '-', {
    //                 itemId: 'delete',
    //                 text: 'Delete',
    //                 iconCls: 'icon-delete',
    //                 disabled: true,
    //                 handler: function(){
    //                     var selection = grid.getView().getSelectionModel().getSelection()[0];
    //                     if (selection) {
    //                             Ext.Msg.show({
    //                                  //title:'确实删除?',
    //                                  message:'确实删除?',
    //                                  buttons: Ext.Msg.YESNO,
    //                                  icon: Ext.Msg.QUESTION,
    //                                  fn: function(btn) {
    //                                      if (btn === 'yes') {
    //                                          store.remove(selection);
    //                                      } else if (btn === 'no') {
    //                                          console.log('No pressed');
    //                                      } else {
    //                                          console.log('Cancel pressed');
    //                                      } 
    //                                  }
    //                            });
    //                     }
    //                 }
    //             }]
    //         }]
    //     });
    //     grid.getSelectionModel().on('selectionchange', function(selModel, selections){
    //         grid.down('#delete').setDisabled(selections.length === 0);
    //     });
    //     return grid;
    // };

    var onAbout=function(){
        console.log("click");
        var helloWindow = new Ext.Window({
            x:0,y:60,
        });
        helloWindow.show('windowDiv');
        helloWindow.add(load_user_edit());//loadUser());
    };
    var onItem=function(){
        console.log("click");
        var helloWindow = new Ext.Window({
            x:0,y:60,
        });
        helloWindow.show('windowDiv');
        helloWindow.add(loadItem());
    }; 
    var onContact=function(){
        console.log("click");
        var helloWindow = new Ext.Window({
            x:0,y:60,
        });
        helloWindow.show('windowDiv');
        helloWindow.add(loadContact());
    }; 
    var onContactItem=function(contact){
        console.log("click");
        var helloWindow = new Ext.Window({
            x:0,y:60,
        });
        helloWindow.show('windowDiv');
        helloWindow.add(loadContactItem(contact));
    }; 
     var selectContactItem=function(contact,store){
        console.log("click");
        var helloWindow = new Ext.Window({
            x:0,y:60,modal:true,
        });
        helloWindow.show('windowDiv');
        helloWindow.add(loadItem(true,store,contact,helloWindow));
    }; 
    var onContactItemTest=function(){
        var contact={id:9,hetongbh:"test"};
        onContactItem(contact);
    }; 
    var onTest=function(){
        var helloWindow = new Ext.Window({
            x:0,y:60,modal:true,
        });
        helloWindow.show('windowDiv');
        helloWindow.add(loadItemNew());
    }; 
    //toolbar//////////////////////////////////////////////////////////////////////
    var tbar = new Ext.Toolbar({
    items:[
       // { text:'檔案', 
       //   iconCls:'file',
       //   menu:[
       //      { text:'開新檔案', iconCls:'new_file' },
       //      { text:'開啓檔案', iconCls:'open_file' },
       //      { text:'儲存檔案', iconCls:'save_file' }
       //   ] 
       // },
       // '-',
       // { text:'編輯',
       //   iconCls:'edit',
       //   menu:[
       //      { text:'複製', iconCls:'copy' },
       //      { text:'剪下', iconCls:'cut' },
       //      { text:'貼上', iconCls:'paste' }
       //   ]
       // },
       { text:'用户', iconCls:'question',handler:onAbout},
       { text:'部件', iconCls:'question',handler:onItem},
       { text:'合同', iconCls:'question',handler:onContact},
       { text:'test', iconCls:'question',handler:onTest},
        ]
    });
       
    var panel = new Ext.Panel({
        title:'装箱单',
        tbar:tbar,
        //width:300,
        //height:200,
        //frame:true, //uncomment to see the result
        renderTo:'container'
    });
    var showLogin=function(){
        var helloWindow = new Ext.Window({
            x:0,y:60,modal:true,
        });
        var loginform=new ui.LoginForm({url:"/rest/login/",token:token,win:helloWindow,userDiv:userDiv});
        var main = Ext.create('Ext.container.Container', {
            padding: '0 0 0 20',
            width: 300,
            height:150,
            renderTo: "loginDiv",
            layout: {
                type: 'vbox',
                align: 'stretch'
            },
            items: [                loginform,
            ]
        });
        helloWindow.show('windowDiv');
        helloWindow.add(main);
    };
    if (user=="AnonymousUser"){
        showLogin();
    }
});
