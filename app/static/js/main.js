$(document).ready( function() {

	//Hide flash

	$('.flash-list').delay(1500).slideUp();

	//Flash result

	function flashResult(result) {
		$('#flash-container').html("<ul class='flash-list'><li class='flash-item'>" + result + "</li></ul>");
		$('.flash-list').delay(1500).slideUp();
	}

	// Profile edit
	$('#info-edit-button').click(function(){
		$('#profile-box').fadeIn();
		$('#main-profile-info').hide();
		$('#edit-info-overlay').hide();
		$('#info-edit-button').hide();
		$('#edit-profile-info').hide();
	});
// isEditingForm = false
	$('.edit-profile-info').hover(function(){
		$('#edit-info-overlay').toggle();
		$('#info-edit-button').toggle();

	});
<<<<<<< HEAD


=======
	//
	// $('#profile-overlay').click(function(){
	// 	$('#profile-overlay').fadeOut();
	// 	$('#profile-overlay-form').fadeOut();
	// });
>>>>>>> ana

	//Navigation menu

	$('.notification-overlay').click(function(){
		var id = $(this).parent().attr('id');
		$(".drop-down:not(#" + id + " .drop-down)").hide();
		$(this).siblings('.drop-down').slideToggle(500);
		$('#menu-line-2').removeClass('active');
		$('#menu-line-1').removeClass('active');
		$('#menu-line-3').removeClass('active');
		if (id == 'search'){
			$('#search-input').focus();
		}
	});

	$('#menu-btn').click(function(){
		$(".drop-down:not(#drop-down-menu)").hide();
		$('#drop-down-menu').slideToggle(500);
		$('#menu-line-2').toggleClass('active');
		$('#menu-line-1').toggleClass('active');
		$('#menu-line-3').toggleClass('active');
	});


	//Search

	$('#search-form').submit(function(e) {
		var name = $("#search-input").val();

		formInput = {
			"name": name
		};

		$.post("/search/",
			formInput,
			function(data) {
				var html = "<ul>";
				if (data.length === 0){
					html += "<li class='no-hover'>Your search did not return any results.</li>";
				} else {
					for (var i = 0; i < data.length; i++){
						html += "<a href='/user/" + data[i].id + "'><li>" + data[i].fname + " " + data[i].lname + "</li></a>";
					}
				}
				html += "</ul>";
				$(".search-drop-down").html(html);
			}
		);
		e.preventDefault();
	});
});
