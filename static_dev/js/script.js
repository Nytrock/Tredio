var num_actors = 0;

$("#addBtn").click(function () {
    num_actors += 1;
    var $div = $("#troupe_member");
    var $klon = $div.clone().attr("class", "row");
    $klon.children("#first_input").children("#actor_change0").attr("name", "actor_change" + num_actors)
    $klon.children("#second_input").children("#role0").attr("name", "role" + num_actors).val("")
    $klon.appendTo("#troupe" );
});

$("#addContBtn").click(function () {
    num_actors += 1;
    var $div = $("#actor_contact");
    var $klon = $div.clone().attr("class", "row");
    $klon.children("#first_input").children("#contact_type0").attr("name", "contact_type" + num_actors)
    $klon.children("#second_input").children("#value0").attr("name", "value" + num_actors).val("").prop("required", true)
    $klon.appendTo("#contacts" );
});

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