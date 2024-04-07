$(".proj_cont").click(function (event) {
  $("#viewer").attr("displayed", true);
  socket.emit("view_project", $(this).data("id"), function (data) {
    $("#viewer_cont").html(data);
  });
});
