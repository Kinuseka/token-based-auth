$(document).ready(function(){
  $("#token-js-create").click(function(event){
    var rand_id = Math.floor(((Math.random() * 10000) + 100));
    $.ajax({
      data : {
        Random : rand_id
      },
      type : 'POST',
      url : '/ne_jax_w'
    })
    .done(function(data) {
      if (data.status == "acknowledged") {
        //var message = (`The request was successfully acknowledged the request from the server\n Server Recieved: ${data.access_id} Client sent: ${rand_id}`);
        //alert(message);
        var link = (`/new`);
        $("#hidden-js-token").attr("action",link);
        $('input[name=sent_value').val(rand_id);
        $("#hidden-js-token").submit();
      }
      else {
        alert(`Failed to start! Reason: ${data.status}`);
      }
       
    })
  });
  event.preventDefault();
});
$(document).ready(function(){
  $("#token_verify").submit(function(event){
    var token_value = $("#token_verify").find('input[name="token"]').val();
    if (token_value == "") {
      $("#warning-js").text("Enter a token or create a new one!");
      return false;
    }
    else if (token_value != ""){
      $.ajax({
      data: {
        token_sent : token_value
      },
      type : "POST",
      url : "/as_jax_token"
    })
      .done(function(data) {
      if (data.response != "valid") {
        alert(`Failed due to reason: ${data.response}`);
      }
    })
    }
  });
});
//segment
function replace() {
        $(document).ready(function() {
          var test = "We do this in order to track user activity for tracking bugs and to try and block malicious activities and etc...";
          $("#Message").html(test);
        });
      }