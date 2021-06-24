$(function(){
   $('.inline-manager_name').editable({
      mode: 'inline',
      url: urls,
      type: 'text',
      name: 'username',  
         validate: function(value) {
         if($.trim(value) == '') return 'This field is required';
      },
      params: function(params) {  // params已经包含`name`，`value`和`pk`
      var data = {};
      data['pk'] = params.pk;
      data['name'] = params.name;
      data['value'] = params.value;
      data['csrf_token'] = csrf;
      return data;
     }
  });

  $('.inline-manager_user_type').editable({
   mode: 'inline',
   url: urls,
   type: 'text',
   name: 'user_type',  
      validate: function(value) {
      if($.trim(value) == '') return 'This field is required';
   },
   params: function(params) {  // params已经包含`name`，`value`和`pk`
    var data = {};
    data['pk'] = params.pk;
    data['name'] = params.name;
    data['value'] = params.value;
    data['csrf_token'] = csrf;
    return data;
  }
});

$('.inline-manager_EMail').editable({
   mode: 'inline',
   url: urls,
   type: 'text',
   name: 'EMail',  
      validate: function(value) {
      if($.trim(value) == '') return 'This field is required';
   },
   params: function(params) {  // params已经包含`name`，`value`和`pk`
    var data = {};
    data['pk'] = params.pk;
    data['name'] = params.name;
    data['value'] = params.value;
    
    data['csrf_token'] = csrf;
    return data;
  }
});
    //inline editables 
    $('.inline-name').editable({
		  mode: 'inline',
        url: urls,
        type: 'text',
        name: 'names',  
           validate: function(value) {
           if($.trim(value) == '') return 'This field is required';
        },
        params: function(params) {  // params已经包含`name`，`value`和`pk`
         var data = {};
         data['pk'] = params.pk;
         data['name'] = params.name;
         data['value'] = params.value;
         
         data['csrf_token'] = csrf;
         return data;
       }
    });
    
    
    $('.inline-sex').editable({
		 mode: 'inline',
         url: urls,
         type: 'select',
         name: 'sex',
        // prepend: "男",
        source: [
            {value: '男', text: '男'},
            {value: '女', text: '女'},
        ],
        display: function(value, sourceData) {
             var colors = {"": "gray", '男': "green", '女': "blue"},
                 elem = $.grep(sourceData, function(o){return o.value == value;});
                 
             if(elem.length) {    
                 $(this).text(elem[0].text).css("color", colors[value]); 
             } else {
                 $(this).empty(); 
             }
        },
        params: function(params) {  // params已经包含`name`，`value`和`pk`
         var data = {};
         data['pk'] = params.pk;
         data['name'] = params.name;
         data['value'] = params.value;
         
         data['csrf_token'] = csrf;
         return data;
       }   
    });    

    $('.inline-education_background').editable({
        mode: 'inline',
        url: urls,
        type: 'text',

        // pk: {{}},
        name: 'education_background',   
           validate: function(value) {
           if($.trim(value) == '') return 'This field is required';
        },
        params: function(params) {  // params已经包含`name`，`value`和`pk`
         var data = {};
         data['pk'] = params.pk;
         data['name'] = params.name;
         data['value'] = params.value;
         
         data['csrf_token'] = csrf;
         return data;
       }
    }); 
    
    $('.dob').editable({
	   mode: 'inline',
       url: urls,
       type: 'combodate',
       name: 'time_of_graduation',
       params: function(params) {  // params已经包含`name`，`value`和`pk`
         var data = {};
         data['pk'] = params.pk;
         data['name'] = params.name;
         data['value'] = params.value;
         
         data['csrf_token'] = csrf;
         return data;
       }
	});
          
$('.inline-school_of_graduation').editable({
    mode: 'inline',
    url: urls,
    type: 'text',

    // pk: {{}},
    name: 'school_of_graduation',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    },
    params: function(params) {  // params已经包含`name`，`value`和`pk`
      var data = {};
      data['pk'] = params.pk;
      data['name'] = params.name;
      data['value'] = params.value;
      
      data['csrf_token'] = csrf;
      return data;
    }
    });    

    $('.inline-major').editable({
    mode: 'inline',
    url: urls,
    type: 'text',

    // pk: {{}},
    name: 'major',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    },
    params: function(params) {  // params已经包含`name`，`value`和`pk`
      var data = {};
      data['pk'] = params.pk;
      data['name'] = params.name;
      data['value'] = params.value;
      
      data['csrf_token'] = csrf;
      return data;
    }
    });

    $('.inline-phone_number').editable({
    mode: 'inline',
    url: urls,
    type: 'text',

    // pk: {{}},
    name: 'phone_number',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    },
    params: function(params) {  // params已经包含`name`，`value`和`pk`
      var data = {};
      data['pk'] = params.pk;
      data['name'] = params.name;
      data['value'] = params.value;
      
      data['csrf_token'] = csrf;
      return data;
    }
    });    
    
    $('.inline-job_wanted').editable({
    mode: 'inline',
    url: urls,
    type: 'text',

    // pk: {{}},
    name: 'job_wanted',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    },
    params: function(params) {  // params已经包含`name`，`value`和`pk`
      var data = {};
      data['pk'] = params.pk;
      data['name'] = params.name;
      data['value'] = params.value;
      
      data['csrf_token'] = csrf;
      return data;
    }
    }); 

    $('.inline-job_time').editable({
    mode: 'inline',
    url: urls,
    type: 'text',

    // pk: {{}},
    name: 'job_time',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    },
    params: function(params) {  // params已经包含`name`，`value`和`pk`
      var data = {};
      data['pk'] = params.pk;
      data['name'] = params.name;
      data['value'] = params.value;
      
      data['csrf_token'] = csrf;
      return data;
    }
    }); 

    $('.inline-salary').editable({
    mode: 'inline',
    url: urls,
    type: 'text',

    // pk: {{}},
    name: 'salary',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    },
    params: function(params) {  // params已经包含`name`，`value`和`pk`
      var data = {};
      data['pk'] = params.pk;
      data['name'] = params.name;
      data['value'] = params.value;
      
      data['csrf_token'] = csrf;
      return data;
    }
    });

    $('.inline-comments').editable({
        showbuttons: 'bottom',
		mode: 'inline',
        url: urls,
        type: 'textarea',
        name: 'resume',
        params: function(params) {  // params已经包含`name`，`value`和`pk`
         var data = {};
         data['pk'] = params.pk;
         data['name'] = params.name;
         data['value'] = params.value;
         
         data['csrf_token'] = csrf;
         return data;
       }
    }); 

    $('.inline-job_type').editable({
    mode: 'inline',
    url: urls,
    type: 'text',

    // pk: {{}},
    name: 'job_type',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    },
    params: function(params) {  // params已经包含`name`，`value`和`pk`
      var data = {};
      data['pk'] = params.pk;
      data['name'] = params.name;
      data['value'] = params.value;
      
      data['csrf_token'] = csrf;
      return data;
    }
    });
    
    $('.inline-company_name').editable({
    mode: 'inline',
    url: urls,
    type: 'text',

    // pk: {{}},
    name: 'company_name',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    },
    params: function(params) {  // params已经包含`name`，`value`和`pk`
      var data = {};
      data['pk'] = params.pk;
      data['name'] = params.name;
      data['value'] = params.value;
      
      data['csrf_token'] = csrf;
      return data;
    }
    });
    $('.inline-brief_introduce').editable({
    mode: 'inline',
    url: urls,
    type: 'text',

    // pk: {{}},
    name: 'brief_introduce',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    },
    params: function(params) {  // params已经包含`name`，`value`和`pk`
      var data = {};
      data['pk'] = params.pk;
      data['name'] = params.name;
      data['value'] = params.value;
      
      data['csrf_token'] = csrf;
      return data;
    }
    });
    $('.inline-address').editable({
    mode: 'inline',
    url: urls,
    type: 'text',

    // pk: {{}},
    name: 'address',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    },
    params: function(params) {  // params已经包含`name`，`value`和`pk`
      var data = {};
      data['pk'] = params.pk;
      data['name'] = params.name;
      data['value'] = params.value;
      
      data['csrf_token'] = csrf;
      return data;
    }
    });
    $('.company_dob').editable({
       mode: 'inline',
       url: urls,
       type: 'combodate',
       name: 'company_dob',
       params: function(params) {  // params已经包含`name`，`value`和`pk`
         var data = {};
         data['pk'] = params.pk;
         data['name'] = params.name;
         data['value'] = params.value;
         
         data['csrf_token'] = csrf;
         return data;
       }
    });
    $('.birth_dob').editable({
       mode: 'inline',
       url: urls,
       type: 'combodate',
       name: 'birth_time',
       params: function(params) {  // params已经包含`name`，`value`和`pk`
         var data = {};
         data['pk'] = params.pk;
         data['name'] = params.name;
         data['value'] = params.value;
         
         data['csrf_token'] = csrf;
         return data;
       }
    });
    $('.inline-workplace').editable({
    mode: 'inline',
    url: urls,
    type: 'text',

    // pk: {{}},
    name: 'workplace',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    },
    params: function(params) {  // params已经包含`name`，`value`和`pk`
      var data = {};
      data['pk'] = params.pk;
      data['name'] = params.name;
      data['value'] = params.value;
      
      data['csrf_token'] = csrf;
      return data;
    }
    });

    $('.inline-company_salary').editable({
    mode: 'inline',
    url: urls,
    type: 'text',

    // pk: {{}},
    name: 'company_salary',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    },
    params: function(params) {  // params已经包含`name`，`value`和`pk`
      var data = {};
      data['pk'] = params.pk;
      data['name'] = params.name;
      data['value'] = params.value;
      
      data['csrf_token'] = csrf;
      return data;
    }
    });
    $('.inline-contact_person').editable({
    mode: 'inline',
    url: urls,
    type: 'text',

    // pk: {{}},
    name: 'contact_person',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    },
    params: function(params) {  // params已经包含`name`，`value`和`pk`
      var data = {};
      data['pk'] = params.pk;
      data['name'] = params.name;
      data['value'] = params.value;
      
      data['csrf_token'] = csrf;
      return data;
    }
    });
    $('.inline-company_phone_number').editable({
    mode: 'inline',
    url: urls,
    type: 'text',

    // pk: {{}},
    name: 'company_phone_number',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    },
    params: function(params) {  // params已经包含`name`，`value`和`pk`
      var data = {};
      data['pk'] = params.pk;
      data['name'] = params.name;
      data['value'] = params.value;
      
      data['csrf_token'] = csrf;
      return data;
    }
    });
    $('.inline-person_num').editable({
    mode: 'inline',
    url: urls,
    type: 'text',

    // pk: {{}},
    name: 'person_num',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    },
    params: function(params) {  // params已经包含`name`，`value`和`pk`
      var data = {};
      data['pk'] = params.pk;
      data['name'] = params.name;
      data['value'] = params.value;
      
      data['csrf_token'] = csrf;
      return data;
    }
    });

    $('.inline-company_comments').editable({
        showbuttons: 'bottom',
        mode: 'inline',
        url: urls,
        type: 'textarea',
        name: 'company_comments',
        params: function(params) {  // params已经包含`name`，`value`和`pk`
         var data = {};
         data['pk'] = params.pk;
         data['name'] = params.name;
         data['value'] = params.value;
         
         data['csrf_token'] = csrf;
         return data;
       }
    });

});