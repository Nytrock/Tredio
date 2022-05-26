let form_count = Number($("[name=field_count]").val());
// get extra form count so we know what index to use for the next item.

function addMultipleField() {
    var $div = $("#multiple_field");
    var $klon = $div.clone();
    $klon.children("#key_stub").attr("name", "key_" + form_count).attr("id", "id_key_" + form_count).prop("required", true);
    $klon.children("#value_stub").attr("name", "value_" + form_count).attr("id", "id_value_" + form_count);
    $klon.appendTo("#multiple_fields");

    form_count++;
    $("[name=field_count]").val(form_count);
    return $klon;
}

$("#addBtn").click(function() {
    $field = addMultipleField();
    $field.attr("class", "row");
})

$("#AddContactProfile").click(function () {
    $field = addMultipleField();
    $field.attr("class", "mb-3");
    $field.children("#id_value_" + form_count - 1).prop("required", true);
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
