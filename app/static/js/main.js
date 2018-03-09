$(document).ready( function() {

	$('.nav-item').click(function(){
		$(this).find('.drop-down').slideToggle(500);
	});
});