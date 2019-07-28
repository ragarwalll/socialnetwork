function checkit() {
  var usernameResponse;
  var usernameCheck = document.querySelector(".user").value;
  if (usernameCheck) {
    $.ajax({
      type: "GET",
      url: "checkusername/",
      data: {
        usernameTrue: usernameCheck
      },
      success: function(data) {
        $("#email_status").html($.trim(data.replace(/[\t\n]+/g, " ")));
      }
    });
  } else {
    $("#email_status").html("");
    return false;
  }
}
