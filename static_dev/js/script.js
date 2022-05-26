let form_count = Number($("[name=field_count]").val());
// get extra form count so we know what index to use for the next item.

$("#addBtn").click(function() {
    var $div = $("#multiple_field");
    var $klon = $div.clone().attr("class", "row");
    $klon.children("#first_input").children("#key_stub").attr("name", "key_" + form_count).attr("id", "id_key_" + form_count).prop("required", true);
    $klon.children("#second_input").children("#value_stub").attr("name", "value_" + form_count).attr("id", "id_value_" + form_count);
    $klon.appendTo("#multiple_fields");

    form_count++;
    $("[name=field_count]").val(form_count);
})

$("#AddContactProfile").click(function () {
    num_actors += 1;
    var $div = $("#contact-div");
    var $klon = $div.clone().attr("class", "mb-3");
    $klon.children("#contact-label").attr("name", "contact-label" + num_actors);
    $klon.children("#contact-text").attr("name", "contact-text" + num_actors).prop("required", true);
    $klon.appendTo("#contact-container");
});

const menuLinks = document.querySelectorAll('.menu_linked[data-goto]');
if (menuLinks.length > 0){
	menuLinks.forEach(menuLink => {
		menuLink.addEventListener("click", onMenuLinkClick);
	});

	function onMenuLinkClick(e){
		const menuLink = e.target;
		if (menuLink.dataset.goto && document.querySelector(menuLink.dataset.goto)){
			const gotoBlock = document.querySelector(menuLink.dataset.goto);
			const gotoBlockValue = gotoBlock.getBoundingClientRect().top + pageYOffset;

			window.scrollTo({
				top: gotoBlockValue,
				behavior: "smooth"
			});
			const iconMenu = document.querySelector('.menu_icon');
			const menuBody = document.querySelector('.menu_body');
			iconMenu.classList.toggle('_active');
			menuBody.classList.toggle('_active');
			if (isMobile.any()){
				let menuArrows = document.querySelectorAll('.menu_link');
				if (menuArrows.length > 0){
					for (let index = 0; index < menuArrows.length; index++){
						const menuArrow = menuArrows[index];
						menuArrow.parentElement.classList.remove("_active");
					}
				}
			}

			e.preventDefault();
		}
	}
}

function postLike(clickedElement) {
    var frm = $(clickedElement).parent().parent();
    var button = $(clickedElement);
    var result = frm.serialize() + '&' + encodeURI(button.attr('name')) + '=' + encodeURI(button.attr('value'));
    $.ajax({
        type: frm.attr('method'),
        url: frm.attr('action'),
        data: result,
        dataType: "json",
        success: function (data) {
            console.log(data);
            var button_like = data.like_num;
            var button_dislike = data.dislike_num;
            if (data.like) {
                if (button.hasClass("btn-primary")){
                    button.attr("class", "btn btn-light like");
                    button.html("<i class='fa fa-thumbs-o-up' aria-hidden='true'> </i> " + (button_like - 1));
                    frm.children("#like_num").attr("value", button_like - 1);
                } else {
                    button.attr("class", "btn btn-primary like");
                    button.html("<i class='fa fa-thumbs-up' aria-hidden='true'> </i> " + (button_like + 1));
                    frm.children("#like_num").attr("value", button_like + 1);
                    dislike = button.parent().children("#dislike");
                    if (dislike.hasClass("btn-danger")) {
                        dislike.html("<i class='fa fa-thumbs-o-down' aria-hidden='true'> </i> " + (button_dislike - 1));
                        frm.children("#dislike_num").attr("value", button_dislike - 1);
                        dislike.attr("class", "btn btn-light like");
                    }
                }
            } else {
                if (button.hasClass("btn-danger")){
                    button.attr("class", "btn btn-light like");
                    button.html("<i class='fa fa-thumbs-o-down' aria-hidden='true'> </i> " + (button_dislike - 1));
                    frm.children("#dislike_num").attr("value", button_dislike - 1)
                } else {
                    button.attr("class", "btn btn-danger like");
                    button.html("<i class='fa fa-thumbs-down' aria-hidden='true'> </i> " + (button_dislike + 1));
                    frm.children("#dislike_num").attr("value", button_dislike + 1);
                    like = button.parent().children("#like");
                    if (like.hasClass("btn-primary")){
                        like.html("<i class='fa fa-thumbs-o-up' aria-hidden='true'> </i> " + (button_like - 1));
                        frm.children("#like_num").attr("value", button_like - 1);
                        like.attr("class", "btn btn-light like");
                    }
                }
            }
        },
    });
    return false;
}

$("#theatre-location").suggestions({
    token: "6063ae24b88df958c4d542fe267af6783a36dd4c",
    type: "ADDRESS",
    onSelect: function(suggestion) {
        $("#location-fias").val(suggestion.data.fias_id)
        $("#location-city").val(suggestion.data.city)
    }
});
