$(document).ready( function() {

	// Profile edit

	$('#info-edit-button').click(function(){
		$('#profile-box').removeClass("hide").addClass("show");
		$('#main-profile-info').removeClass("show").addClass("hide");
		$('#edit-info-overlay').hide();
		$('#info-edit-button').hide();
		$('#info-edit-button').removeClass("active");
	});


	$('.edit-profile-info').hover(function(){
		if ($('#info-edit-button').hasClass("active")) {
			$('#edit-info-overlay').toggle();
			$('#info-edit-button').toggle();
		}
	});

	$('#cancel-edit').click(function() {
		$('#profile-box').removeClass("show").addClass("hide");
		$('#main-profile-info').removeClass("hide").addClass("show");
		$('#edit-info-overlay').show();
		$('#info-edit-button').show();
		$('#info-edit-button').addClass("active");
	});


	//Availability editing

	$('#edit-box-button').click(function(){
		$('#avail_user').hide();
		$('#avail_form').show();
	});

	$('.daybox-blue').hover(function(){
		$(this).find('.avail_user').toggle();
	});

	$('.availability-info').hover(function(){
		if ($('#avail-edit-button').hasClass("active")) {
			$('#edit-avail-overlay').toggle();
			$('#avail-edit-button').toggle();
		}
	});

	$('#avail-edit-button').click(function(){
		$('.edit-day-box').removeClass("hide").addClass("show");
		$('#avail-edit-button').removeClass("active");
		$('#edit-avail-overlay').hide();
		$('#avail-edit-button').hide();
	});

	//Removing availability

	$(".remove-availability-form").submit(function(e) {
		e.preventDefault();
		var url = $(this).attr("action");
		var avail_id = $(this).data("availid");
		var target = "#avail-container-" + avail_id;

		$.post(url,
			function(data) {
				if (data["status"] == "success"){
					$(target).fadeOut();
				} else {
					flashResult("An error occured.");
				}
			}
		);
	});

});