var num_actors = 0;

$('#addBtn').click(function () {
    num_actors += 1;
    var $div = $("#troupe_member");
    var $klon = $div.clone().attr("class", "row");
    $klon.children("#first_input").children("#actor_change0").attr("name", "actor_change" + num_actors)
    $klon.children("#second_input").children("#role0").attr("name", "role" + num_actors).val("")
    $klon.appendTo("#troupe" );
});