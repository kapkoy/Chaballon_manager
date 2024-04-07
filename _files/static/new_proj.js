var new_user = false;
var date = new Date().toISOString().substr(0, 10);

if ($("#new_proj_start").val() == "") {
  $("#new_proj_start").val(date);
  $("#new_proj_end").val(date);
}

function close_dialog() {
  $("#create_dialog").css("display", "none");
  $("#fat-container").css("filter", "blur(0)");
}

$("form").submit(function (e) {
    let edit = ($(this).attr("edit") != undefined);
console.log(edit);
    let id = $("#new_proj_cont #proj_id").text().replace("- ","");
  let name = $("#new_proj_name input").val();
  let start = $("#new_proj_start").val();
  let end = $("#new_proj_end").val();
  let user = $("#user_select").val();

  let this_user = null;
  if (new_user) {
    console.log(new_user)
    let u_fname = $("input[name='firstname']").val();
    let u_lname = $("input[name='lastname']").val();
    let u_mail = $("input[name='mail']").val();
    let u_phone = $("input[name='phone']").val();
    let u_address = $("input[name='address']").val();
    this_user = {
      firstname: u_fname,
      lastname: u_lname,
      phone: u_phone,
      mail: u_mail,
      address: u_address
    };
  }

  socket.emit(
    "new_proj",
    { name: name, start: start, end: end, user: user, new_user: this_user, edit:edit, id:id },
    function (data) {
      close_dialog();
      $("#viewer_cont").html(data);
    }
  );
  return false;
});

$("#create_dialog").click(function (e) {
  if (e.target == e.currentTarget) {
    close_dialog();
  }
});

$("#new_client_btn").click(function (e) {
  let edit = $(this).attr("edit");

  if (!new_user) {
    $("#new_client_cont").show();
    $("#new_client_cont input .requiered").attr("required", "");

    if (edit == undefined) {
      $("#user_select").attr("disabled", "");
      console.log("caca");
      $("#user_select").val("-- Nouveau Client --");
    }
    new_user = true;
  } else {
    $("#new_client_cont").hide();
    $("#new_client_cont input .requiered").removeAttr("required");

    if (edit == undefined) {
      $("#user_select").removeAttr("disabled");
      $("#user_select option:nth-child(1)").attr("selected", "");
    }
    new_user = false;
  }
});

