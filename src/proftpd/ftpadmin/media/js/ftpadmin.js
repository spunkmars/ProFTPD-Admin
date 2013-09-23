    function fill_selected_value(form,status){
       var value_str;
       var selected_count=0;
       var elements = form.getElementsByTagName('input');
       for(var i=0; i<elements.length; i++){
            if(elements[i].type == 'checkbox'){
                if(elements[i].checked==true){
                    ++selected_count;
                    if (typeof(value_str) == 'undefined'){
                        value_str = elements[i].value;
                    }else{
                        value_str = value_str + ',' + elements[i].value;
                    }
                }
            }
        }
        form.select_across.value = value_str;
        document.getElementById("selected_count").innerHTML= selected_count + " item selected"
    }



    function checkAll(form1,status){              
        var elements = form1.getElementsByTagName('input');  
        for(var i=0; i<elements.length; i++){  
            if(elements[i].type == 'checkbox'){  
                if(elements[i].checked==false){  
                    elements[i].checked=true;  
                }  
            }  
        } 
        fill_selected_value(form1,status);    
    }  
    function switchAll(form1,status){             
        var elements = form1.getElementsByTagName('input');  
        for(var i=0; i<elements.length; i++){  
            if(elements[i].type == 'checkbox'){  
                if(elements[i].checked==true){  
                    elements[i].checked=false;  
                }else if(elements[i].checked==false){  
                    elements[i].checked=true;  
                }  
            }  
        }
        fill_selected_value(form1,status); 
    }  
    function uncheckAll(form1,status){    
        var elements = form1.getElementsByTagName('input');       
        for(var i=0; i<elements.length; i++){                     
            if(elements[i].type == 'checkbox'){               
                if(elements[i].checked==true){                    
                    elements[i].checked=false;                    
                }  
            }  
        } 
        fill_selected_value(form1,status);    
    } 

 

function openprompt(confirm_msg, callback){
    /* var str = confirm_msg(); */
    var str = confirm_msg;
    $.prompt(str,{
            buttons: { Ok: true, Cancel: false },
            focus: 1,
            callback: function(e,v,m,f){ 
                if (v == true) {
                    callback();
                }
            }
    });
};

