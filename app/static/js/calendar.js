$(document).ready( function() {

	//Style today's date calendar

	var urlArr = window.location.href.split("/");
	var urlLen = urlArr.length;
	var calMonth = urlArr[urlLen - 1];
	var calYear = urlArr[urlLen - 2];
	var today = new Date();
	var tdArr = $( ".calendar td" ).toArray();

	for (var i = 0; i < tdArr.length; i++) {
		var td = $(tdArr[i]);
		var day = td.find('.date-val').html();
		var date = new Date(calYear, calMonth - 1, day);

		if (date.getDate() == today.getDate() && date.getMonth() == today.getMonth() && date.getYear() == today.getYear()){
			td.css('background-color', "E2E2E2");
		}
	}

	//Calendar overlay

	$('.add-btn').click(function(){
		$('.overlay').fadeIn();
		$('#new-event-overlay-form').fadeIn();
	});

	function hideOverlay(){
		$('.overlay').fadeOut();
		$('.overlay-form').fadeOut();
	}

	$('.close-btn').click(function() {
		hideOverlay();
	});

	$('.overlay').click(function() {
		hideOverlay();
	});

	$('#cal-event-overlay-form .close-btn').click(function() {
		window.location.replace("/calendar/" + calYear + "/" + calMonth);
	});


	//New event - calendar page

	$('#create-calendar-event-form').submit(function(e) {
		var url = $(this).attr("action");
		$.ajax({
			type: "POST",
			url: url,
			data: $(this).serialize(),
			success: function(data) {
				if(data[0] == "error"){
					validationErrors(data[1], true);
				} else if (data[0] == "success"){
					window.location.replace("/calendar/" + calYear + "/" + calMonth);
				}
			}
		});
		e.preventDefault();
	});

});