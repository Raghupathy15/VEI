odoo.define('vg_colg.student_admission', function (require) {
'use strict';

    var ajax= require('web.ajax')

    $( document ).ready(function() {

        $(document).on('change', '#aadharcard', function(){

          const aadharCardNumber = document.getElementById('aadharcard').value;
          ajax.jsonRpc('/aadhaarcard', 'call', {'addhar':aadharCardNumber}).then(function(data) {
                if(data){
                    if(confirm("The entered Aadhar No is already registered.")){
                        location.reload();
                    }
                    else{
                        location.reload();
                    }
                }
            })

        });

        $(document).on('change', '#stream_by_id', function(){
          
          const stream = document.getElementById('stream_by_id').value;
          console.log(stream);
          ajax.jsonRpc('/stream', 'call', {'stream':stream}).then(function(data) {
                if (data) {
                  // Here, `options` is the list of tuples you received from the server
                  const otherField = document.getElementById('company_by_id');
                  otherField.innerHTML = ''; // Clear existing options
                  const optionTag = document.createElement('option');
                      optionTag.value = null;
                      optionTag.textContent = null;
                      otherField.appendChild(optionTag);
                  data.forEach(function(option) {
                      const optionTag = document.createElement('option');
                      optionTag.value = option[1];
                      optionTag.textContent = option[0];
                      otherField.appendChild(optionTag);
                  });
              }
              console.log(data);
            })

        });

        $(document).on('change', '#company_by_id', function(){
          
          const company = document.getElementById('company_by_id').value;
          const stream = document.getElementById('stream_by_id').value;
          console.log(company);
          ajax.jsonRpc('/company', 'call', {'company':{'company':company,'stream':stream}}).then(function(data) {
                if (data) {
                  // Here, `options` is the list of tuples you received from the server
                  const otherField = document.getElementById('grade_id');
                  otherField.innerHTML = ''; // Clear existing options
                  const optionTag = document.createElement('option');
                      optionTag.value = null;
                      optionTag.textContent = null;
                      otherField.appendChild(optionTag);
                  data.forEach(function(option) {
                      const optionTag = document.createElement('option');
                      optionTag.value = option[1];
                      optionTag.textContent = option[0];
                      otherField.appendChild(optionTag);
                  });
              }
              console.log(data);
            })

        });

        $(document).on('change', '#grade_id', function(){
          
          const grade = document.getElementById('grade_id').value;
          const stream = document.getElementById('stream_by_id').value;
          console.log(grade);
          ajax.jsonRpc('/grade', 'call', {'company':{'grade':grade,'stream':stream}}).then(function(data) {
                if (data) {
                  // Here, `options` is the list of tuples you received from the server
                  const otherField = document.getElementById('degree_id');
                  otherField.innerHTML = ''; // Clear existing options
                  const optionTag = document.createElement('option');
                      optionTag.value = null;
                      optionTag.textContent = null;
                      otherField.appendChild(optionTag);
                  data.forEach(function(option) {
                      const optionTag = document.createElement('option');
                      optionTag.value = option[1];
                      optionTag.textContent = option[0];
                      otherField.appendChild(optionTag);
                  });
              }
              console.log(data);
            })

        });

        $(document).on('change', '#degree_id', function(){
          
          const grade = document.getElementById('grade_id').value;
          const stream = document.getElementById('stream_by_id').value;
          const company = document.getElementById('company_by_id').value;

          console.log(grade);
          ajax.jsonRpc('/degree', 'call', {'company':{'grade':grade,'stream':stream,'company':company}}).then(function(data) {
                if (data) {
                  // Here, `options` is the list of tuples you received from the server
                  const otherField = document.getElementById('courses_id');
                  otherField.innerHTML = ''; // Clear existing options
                  const optionTag = document.createElement('option');
                      optionTag.value = null;
                      optionTag.textContent = null;
                      otherField.appendChild(optionTag);
                  data.forEach(function(option) {
                      const optionTag = document.createElement('option');
                      optionTag.value = option[1];
                      optionTag.textContent = option[0];
                      otherField.appendChild(optionTag);
                  });
              }
              console.log(data);
            })

        });

        $("#std_email").keyup(function(){
      let form = document.getElementById('stdCreated')
      let kyc_owner_name_email2 = document.getElementById('std_email').value
      let text = document.getElementById('email2')
      let pattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/

      if (kyc_owner_name_email2.match(pattern)) {
        form.classList.add('valid')
        form.classList.remove('invalid')
        text.innerHTML = "Your Email Address is valid"
        text.style.color = '#1ca31c'
        text.style.position = 'absolute'
        text.style.padding = '0px'
      }
      else {
        form.classList.remove('valid')
        form.classList.add('invalid')
        text.innerHTML = "Please Enter Valid Email Address"
        text.style.color = '#ff0000'
        text.style.position = 'absolute'
        text.style.padding = '0px'
      }

      if (kyc_owner_name_email2 == '') {
        form.classList.remove('valid')
        form.classList.remove('invalid')
        text.innerHTML = ""
        text.style.color = '#00ff00'
        text.style.position = 'none'
      }
    })
});

});