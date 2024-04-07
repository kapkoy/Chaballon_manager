var socket = io.connect("http://" + document.domain + ":" + location.port);

$(".noresult").hide();

function sort_hidden(hidden) {
  let toremove = ["Cancel", "Done", "Pause"];
  $(".proj_cont").each(function (index) {
    if (!hidden) {
      let status = $(this).data("status");
      if ($.inArray(status, toremove) != -1) {
        $(this).hide();
      }
    } else {
      $(this).show();
    }
  });
}

$("#hide-button").click(function () {
  if ($(this).is("[shown]")) {
    $(this).removeAttr("shown");
    sort_hidden(false);
  } else {
    $(this).attr("shown", true);
    sort_hidden(true);
  }
});
sort_hidden($("#hide-button").is("[shown]"));



$("#searchbar").on("input", function (event) {
  let search_term = $(this).val();
 
  function filter_search(is_in) {
    return function (index, element) {
      console.log(element);
      return (
        ($(element).data("search").toLowerCase().indexOf(search_term.toLowerCase()) === -1) != is_in);
    };
  }

  $to_show = $(".proj_cont").filter(filter_search(true));
  if ($to_show.length == 0) {
    $(".noresult").show();
  } else {
    $(".noresult").hide();
  }

  if (search_term.length > 0) {
    $to_show.show();
    $(".proj_cont").filter(filter_search(false)).hide();
  } else {
    $(".proj_cont").show();
  }
});

$(".sort_btn").click(function (event) {
  let key = $(this).data("key");
  let invert = $(this).data("invert");
  $(this).data("invert", !invert);
  console.log(invert);
  socket.emit("sort_projects", key, invert);
});

socket.on("refresh_projs", function (data) {
  $("#projects_scroller").html(data);
  sort_hidden($("#hide-button").is("[shown]"));
});

$("#add_proj_btn").click(function (event) {
  socket.emit('new_proj_req', false, function(data){

    $("#create_dialog").css('display', 'flex');
    $("#fat-container").css("filter", "blur(.75rem)")
    $("#create_dialog").html(data);
  });

});






/*
function resize(){
    let decal = $("#header").outerHeight() + $("#proj_topbar").outerHeight()+8; 
    
    let max = $("body").height() * .9;
    console.log($("#projects_scroller")[0].scrollHeight);
    let min = $("#projects_scroller")[0].scrollHeight + decal;
    $("#fat-container").css("height", "min("+min+"px, 90%)");
}
resize();
$( window ).on( "resize", function() {
    resize();
    
  } );
*/
