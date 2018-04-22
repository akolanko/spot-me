$(document).ready( function() {

	// Profile edit

	$('#info-edit-button').click(function(){
		$('#profile-box').fadeIn();
		$('#main-profile-info').hide();
		$('#edit-info-overlay').hide();
		$('#info-edit-button').hide();
		$('#edit-profile-info').hide();
		$('#info-edit-button').removeClass("active");
		$('.edit-profile-info').css('height', '340px');
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
});