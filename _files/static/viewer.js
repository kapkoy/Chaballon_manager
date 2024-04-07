var start_str = $("#time_start").text();
var end_str = $("#time_end").text();
start_str = start_str.split("-");
start_str = start_str[2] + "-" + start_str[1] + "-" + start_str[0];
end_str = end_str.split("-");
end_str = end_str[2] + "-" + end_str[1] + "-" + end_str[0];
console.log(start_str, end_str);

var start = new Date(start_str + " GMT-0100").valueOf();

var end = new Date(end_str + " GMT-0100").valueOf();
var now = new Date();
now = new Date(
  now.getFullYear() +
    "-" +
    (now.getMonth() + 1) +
    "-" +
    now.getDate() +
    " GMT-0100"
).valueOf();

console.log(start, end, now);
var fit = (now - start) / (end - start);
var remaining_days = Math.floor(
  new Date(end - now).valueOf() / 1000 / 60 / 60 / 24
);

$("#progressbar").css("width", Math.min(Math.max(fit * 100, 0), 100) + "%");
if (fit < 1 && fit >= 0) {
  $("#progressbar_cont p").html(remaining_days + " jour(s) restant(s)");
} else if (fit > 1) {
  $("#progressbar_cont p").html("Projet fini (normalement)");
} else if (fit == 1 || isNaN(fit)) {
  $("#progressbar").css("width", "100%");
  $("#progressbar_cont p").html("AUJOURD'HUI !!");
} else {
  $("#progressbar_cont p").html("Pas normal ça..");
}

$("#open_file").click(function (e) {
  console.log($("#v_proj_id").html());
  socket.emit("open_files", $("#v_proj_id").text());
});

$("#other_projs li").click(function (event) {
  $("#viewer").attr("displayed", true);
  socket.emit("view_project", $(this).data("id"), function (data) {
    $("#viewer_cont").html(data);
  });
});

$("#other_projs_cont").on("wheel", function (e) {
  e.preventDefault();
  this.scrollBy({
    left: e.originalEvent.deltaY < 0 ? -50 : 50,
  });
});

$("#viewer_edit_btn").click(function (e) {
  let proj_id = $("#v_proj_id").text();
  socket.emit("new_proj_req", proj_id, function (data) {
    $("#create_dialog").css("display", "flex");
    $("#fat-container").css("filter", "blur(.75rem)");
    $("#create_dialog").html(data);
  });
});

$("#paid_btn").click(function (e) {
  let paid = $(this).attr("paid") == undefined;
  if(paid){
    $(this).attr("paid", "");
  } else {
    $(this).removeAttr("paid");
  }
  console.log(paid);
  socket.emit("update_paid", paid, $("#v_proj_id").text());
});
