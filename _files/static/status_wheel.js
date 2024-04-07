function mapValue(value, fromMin, fromMax, toMin, toMax) {
    // First, normalize the value between 0 and 1 based on the input range
    const normalizedValue = (value - fromMin) / (fromMax - fromMin);
    
    // Then, map the normalized value to the output range
    const result = (normalizedValue * (toMax - toMin)) + toMin;
    
    // Ensure the result is within the specified bounds
    return Math.min(Math.max(result, toMin), toMax);
}

var mousedown = false;

$("#stats_cont").on("mousedown", function(e){
    e.preventDefault();
    let stats = $(this).find(".status_selector");

    mousedown = true;

    let max = stats.length;
    console.log(max)
    stats.each(function(idx, elem){
        let mapped = mapValue(idx, 0, max, -Math.PI, Math.PI);
        let split = 47.5;
        let x = Math.sin(mapped)*split;
        let y = Math.cos(mapped)*split;
        //$(elem).css("transform", "translate("+x+"px,"+y+"px)");
        $(elem).css("transform", "translate("+idx * 42.5+"px,0px)")
        $(elem).css("opacity", "1");
        

    });
});

$("body").on("mouseup", function(e){
    if (mousedown) {
        mousedown = false;
        $(this).find(".status_selector").css("transform", "translate(0,0)");
        $(".status_selector").css("z-index", 0);
        $(".status_selector").css("opacity", 0);
        selected.css("z-index", 100);
        selected.css("opacity", 1);
    
    
        socket.emit("update_status", selected.data("status"), $("#v_proj_id").text());
    }

});

var selected = null;
$(".status_selector").on("mouseover", function(e){
    if (mousedown) {
        selected = $(this);
        $(".status_selector").css("z-index", 0);
        selected.css("z-index", 100);
    }
});