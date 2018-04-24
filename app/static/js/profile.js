$(document).ready( function() {

	// Profile edit

	$('#info-edit-button').click(function(){
		$('#profile-box').fadeIn();
		$('#main-profile-info').hide();
		$('#edit-info-overlay').hide();
		$('#info-edit-button').hide();
		$('#edit-profile-info').hide();
		$('#info-edit-button').removeClass("active");
		$('.edit-profile-info').css('height', '380px');
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
		$('.edit-profile-info').css('height', '290px');
	});

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

});