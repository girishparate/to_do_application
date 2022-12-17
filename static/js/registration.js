$("#pass").keyup(function(){
    var password = $("#pass").val()
    var password_conf = $("#confirm_pass").val()
    if (password==password_conf){
        $("#registration_submit").prop("disabled", false);
    }
  });

  $("#confirm_pass").keyup(function(){
    var password = $("#pass").val()
    var password_conf = $("#confirm_pass").val()
    if (password==password_conf){
        $("#registration_submit").prop("disabled", false);
    }
  });