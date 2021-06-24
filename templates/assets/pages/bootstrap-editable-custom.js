$(function(){
  

    //inline editables 
    $('.inline-name').editable({
		mode: 'inline',
        url: 'http://www.baidu.com',
        type: 'text',

        // pk: {{}},
        name: 'names',
        csrf: 'vdfsvfdfd',   
           validate: function(value) {
           if($.trim(value) == '') return 'This field is required';
        }
    });
    
    
    $('.inline-sex').editable({
		 mode: 'inline',
         url: 'http://www.baidu.com',
         type: 'select',
         name: 'sex',
        // prepend: "男",
        source: [
            {value: 1, text: '男'},
            {value: 2, text: '女'}
        ],
        display: function(value, sourceData) {
             var colors = {"": "gray", 1: "green", 2: "blue"},
                 elem = $.grep(sourceData, function(o){return o.value == value;});
                 
             if(elem.length) {    
                 $(this).text(elem[0].text).css("color", colors[value]); 
             } else {
                 $(this).empty(); 
             }
        }   
    });    
    
    
    
    $('.inline-education_background').editable({
        mode: 'inline',
        url: 'http://www.baidu.com',
        type: 'text',

        // pk: {{}},
        name: 'education_background',   
           validate: function(value) {
           if($.trim(value) == '') return 'This field is required';
        }
    }); 
    
    $('.dob').editable({
	   mode: 'inline',
       url: 'http://www.baidu.com',
       type: 'combodate',
       name: 'time_of_graduation',
	});
          
$('.inline-school_of_graduation').editable({
    mode: 'inline',
    url: 'http://www.baidu.com',
    type: 'text',

    // pk: {{}},
    name: 'school_of_graduation',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    }
    });    

    $('.inline-major').editable({
    mode: 'inline',
    url: 'http://www.baidu.com',
    type: 'text',

    // pk: {{}},
    name: 'major',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    }
    });

    $('.inline-phone_number').editable({
    mode: 'inline',
    url: 'http://www.baidu.com',
    type: 'text',

    // pk: {{}},
    name: 'phone_number',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    }
    });    
    
    $('.inline-job_wanted').editable({
    mode: 'inline',
    url: 'http://www.baidu.com',
    type: 'text',

    // pk: {{}},
    name: 'job_wanted',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    }
    }); 

    $('.inline-job_time').editable({
    mode: 'inline',
    url: 'http://www.baidu.com',
    type: 'text',

    // pk: {{}},
    name: 'job_time',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    }
    }); 

    $('.inline-salary').editable({
    mode: 'inline',
    url: 'http://www.baidu.com',
    type: 'text',

    // pk: {{}},
    name: 'salary',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    }
    });

    $('.inline-comments').editable({
        showbuttons: 'bottom',
		mode: 'inline',
        url: 'http://www.baidu.com',
        type: 'textarea',
        name: 'resume',
    }); 
    




    $('.inline-job_type').editable({
    mode: 'inline',
    url: 'http://www.baidu.com',
    type: 'text',

    // pk: {{}},
    name: 'job_type',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    }
    });
    
    $('.inline-company_name').editable({
    mode: 'inline',
    url: 'http://www.baidu.com',
    type: 'text',

    // pk: {{}},
    name: 'company_name',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    }
    });
    $('.inline-brief_introduce').editable({
    mode: 'inline',
    url: 'http://www.baidu.com',
    type: 'text',

    // pk: {{}},
    name: 'brief_introduce',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    }
    });
    $('.inline-address').editable({
    mode: 'inline',
    url: 'http://www.baidu.com',
    type: 'text',

    // pk: {{}},
    name: 'address',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    }
    });
    $('.company_dob').editable({
       mode: 'inline',
       url: 'http://www.baidu.com',
       type: 'combodate',
       name: 'company_dob',
    });
    $('.birth_dob').editable({
       mode: 'inline',
       url: 'http://www.baidu.com',
       type: 'combodate',
       name: 'birth_time',
    });
    $('.inline-workplace').editable({
    mode: 'inline',
    url: 'http://www.baidu.com',
    type: 'text',

    // pk: {{}},
    name: 'workplace',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    }
    });

    $('.inline-company_salary').editable({
    mode: 'inline',
    url: 'http://www.baidu.com',
    type: 'text',

    // pk: {{}},
    name: 'company_salary',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    }
    });
    $('.inline-contact_person').editable({
    mode: 'inline',
    url: 'http://www.baidu.com',
    type: 'text',

    // pk: {{}},
    name: 'contact_person',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    }
    });
    $('.inline-company_phone_number').editable({
    mode: 'inline',
    url: 'http://www.baidu.com',
    type: 'text',

    // pk: {{}},
    name: 'company_phone_number',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    }
    });
    $('.inline-person_num').editable({
    mode: 'inline',
    url: 'http://www.baidu.com',
    type: 'text',

    // pk: {{}},
    name: 'person_num',   
       validate: function(value) {
       if($.trim(value) == '') return 'This field is required';
    }
    });


    $('.inline-company_comments').editable({
        showbuttons: 'bottom',
        mode: 'inline',
        url: 'http://www.baidu.com',
        type: 'textarea',
        name: 'company_comments',
    });


	
   
});