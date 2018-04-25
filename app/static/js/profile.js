$(document).ready( function() {

	// Profile edit

	$('#info-edit-button').click(function(){
		$('#profile-box').fadeIn();
		$('#main-profile-info').hide();
		$('#edit-info-overlay').hide();
		$('#info-edit-button').hide();
		$('#edit-profile-info').hide();
		$('#info-edit-button').removeClass("active");
	});


	$('.edit-profile-info').hover(function(){
		if ($('#info-edit-button').hasClass("active")) {
			$('#edit-info-overlay').toggle();
			$('#info-edit-button').toggle();
		}
	});

	$('#cancel-edit').click(function() {
		$('#profile-box').hide();
		$('#main-profile-info').show();
		$('#edit-info-overlay').show();
		$('#info-edit-button').show();
		$('#edit-profile-info').show();
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
		$('.edit-day-box').show();
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