odoo.define('insys.access.readonly',function(require){
    "use static"

    var BasicRenderWidget = require('web.BasicRenderer');
    var FormControllerWidget = require('web.FormController')
    var ajax = require('web.ajax');

    FormControllerWidget.include({
        on_attach_callback:function(){
            this._super.apply(this,arguments)
            if(this.modelName=='res.users' && $('.insys_readonly_widget').length>0){
                this._rpc({
                        model:'res.users',
                        method: 'check_user_group' 
                            }).then(function(result){
                                var acccess_page_link = $('.insys_readonly_widget').find('a').attr('href')
                                if (result != true && acccess_page_link != undefined){
                                    var acccess_page_link = acccess_page_link.slice(1,) 
                                    $(`#${acccess_page_link}`).find('.o_inner_group').find('select').attr('disabled','true')
                                    $(`#${acccess_page_link}`).find('.o_inner_group').find('input').attr('disabled','true')
                    
                                }
                            })
            
                }
        }
    })

    BasicRenderWidget.include({
        
        _render:function(){
            var self = this;
            var res = this._super.apply(this,arguments).then(function(data){
                if(self.state.model=='res.users' && $('.insys_readonly_widget').length>0){
                    self._rpc({
                            model:'res.users',
                            method: 'check_user_group' 
                                }).then(function(result){
                                    var acccess_page_link = $('.insys_readonly_widget').find('a').attr('href')
                                    if (result != true && acccess_page_link != undefined){
                                        var acccess_page_link = acccess_page_link.slice(1,) 
                                        $(`#${acccess_page_link}`).find('.o_inner_group').find('select').attr('disabled','true')
                                        $(`#${acccess_page_link}`).find('.o_inner_group').find('input').attr('disabled','true')
                        
                                    }
                                })
                
                    }
                });
    
            return res
            
        }

})
})