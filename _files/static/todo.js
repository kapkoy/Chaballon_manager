var dragElement = null;

$("ul").on("dragstart", ".draghandle", function (event) {
  $(this).parent().css("opacity", ".5");
  dragElement = $(this).parent();
  event.originalEvent.dataTransfer.effectAllowed = "move";
  event.originalEvent.dataTransfer.setData(
    "text/html",
    $(this).parent().html()
  );
});

$("ul").on("dragover", "li", function (event) {
  if (event.preventDefault) {
    event.preventDefault(); // Necessary. Allows us to drop.
  }
  event.originalEvent.dataTransfer.dropEffect = "move"; // See the section on the DataTransfer object.
  if (!$(this).hasClass("tmp_drag")) {
    let pos = event.pageY - $(this).offset().top;
    let height = $(this).outerHeight();
    if (pos < height / 2) {
      $(this).before(dragElement.addClass("tmp_drag"));
    } else {
      $(this).after(dragElement.addClass("tmp_drag"));
    }
  }
  return false;
});

$("ul").on("drop", "li", function (event) {
  dragElement.css("opacity", "1");
  dragElement.removeClass("tmp_drag");

  if (dragElement != $(this)) {
    let pos = event.pageY - $(this).offset().top;
    let height = $(this).outerHeight();
    if (pos < height / 2) {
      $(this).before(dragElement);
    } else {
      $(this).after(dragElement);
    }
  }
  updateTodo()

  return false;
});

$("li").on("dragend", function (event) {
  dragElement.css("opacity", "1");
  dragElement.removeClass("tmp_drag");
  return false;
});

function updateTodo(){
  let todos = [];
  let proj_id = $("#v_proj_id").text();
  $("#todolist .textinput").each(function (data){
    let value = $(this).val();
    if (value.trim() == ""){
      $(this).parent().remove()
    } else {
      let this_todo = {"text":value, "checked": $(this).parent().find(".checkinput").prop("checked")};
      todos.push(this_todo);
    }
    
  });

  socket.emit('new_todo', todos, proj_id);
}


$(".textinput").on('change', function (event) {
    updateTodo()
    $(this).attr('value', $(this).val().trim());
    $(this).val($(this).attr('value'));
});

$("#todos_form").submit(function (e) {
    $focused = $(".textinput:focus");
    if ($focused.val()==""){
        $focused.parent().remove();
    } else {
        $focused.blur();
    }
    return false;
});

$("#new_todo_cont").submit(function(e){
  $input = $(this).find("input");
  let value = $input.val().trim();

  let $elem = $("#todo_template").clone(true, true).addClass("todo_item").removeAttr('id').show();

  $elem.find('.textinput').val(value);
  $elem.find('.textinput').attr('value', value);

  $("#todolist").append($elem);
  $input.val("");
  updateTodo()

  return false;
});


$(".checkinput").on('change', function (event) {
    console.log("click")
    if( $(this).prop('checked')){
        $(this).parent().find('.textinput').attr("checked",true);
    } else {
        $(this).parent().find('.textinput').removeAttr("checked");
    }
    updateTodo()
});
