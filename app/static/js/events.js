$(document).ready( function() {

	//New event - event page

	$('#create-event-form').submit(function(e) {
		var url = $(this).attr("action");
		$.ajax({
			type: "POST",
			url: url,
			data: $(this).serialize(),
			success: function(data) {
				if(data[0] == "error"){
					validationErrors(data[1], true);
				} else if (data[0] == "success"){
					window.location.replace("/event/" + data[1]);
				}
			}
		});
		e.preventDefault();
	});


	//Viewing a notification

	$(".view-notification-form").submit(function(e) {
		e.preventDefault();

		var notification_id = $(this).find(".notification-id").data("notificationid");
		var event_id = $(this).find(".event-id").data("eventid");

		var formInput = {
			"notification_id": notification_id
		};

		$.post("/view_notification/",
			formInput,
			function() {
				window.location.replace("/event/" + event_id);
			}
		);
	});


	//Updating an event

	function updateEvent() {
		$('#edit-event-btn').click(function(){
			$('#event-main').hide();
			$('#update-event').show();
		});

		$('#update-event-form').submit(function(e) {
			$(".error-container").empty();
			var url = $(this).attr("action");
			$.ajax({
				type: "POST",
				url: url,
				data: $(this).serialize(),
				success: function(data) {
					if (data[0] == "error") {
						validationErrors(data[1], true);
					} else {
						$('#update-event').hide();
						$('#event-main').show();
						updateData(data[1]);
					}
				}
			});
			e.preventDefault();
		});
	}
	updateEvent();


	//Accepting an event invitation

	$(".accept-invitation-form").submit(function(e) {
		e.preventDefault();

		var action = $(this).attr("action");
		var event_id = $("#event-title").data("eventid");
		var invite = $("#invite-list").find("[data-eventid='" + event_id + "']");
		var user_id = $(".user-details").data("userid");
		var user_event_id = $("#event-title").data("usereventid");

		$.post(action,
			function(result) {
				flashResult(result[0]);
				invite.hide();

				if ($('.invites').has('.invitation-detail').length) {
					$('.invites .invitation-detail').hide();
					html = "<h2 class='page-title'>Invited</h2><ul>";
					for (i = 0; i < result[1].length; i++) {
						if (result[1][i]["user"].id != user_id){
							html += "<li class='invited-user'><a href='user/" + result[1][i]["user"].id + "'>" + result[1][i]["user"].fname + " " + result[1][i]["user"].lname + " - ";
							if (result[1][i]["user_event"].accepted === 0) {
								html += "Pending";
							} else {
								html += "Accepted";
							}
							html += "</a></li>";
						}
					}
					html += "</ul>";
					$('.invites').prepend(html);
				}
				$('.invites .event-buttons').hide();
				// $('.adding-friends-hidden').show();

				btns = "<div class='event-buttons inline-buttons' id='event-btns-main'><button class='button button-1' id='edit-event-btn'>Edit</button><form onsubmit='return confirm(\"Are you sure you want to remove yourself from this event?\");' class='remove-event-form' action='/remove_event/" + user_event_id + "/' method='post'><button type='submit' class='button button-4'>Remove</button></form></div>";
				$("#event-main").append(btns);

				if( $('#invite-list').height() === 0 ) {
					$('#invite-list').html("<div class='no-results'>You do not currently have any event invitations.</div>");
				}
				updateEvent();
			}
		);
	});


	//Inviting more friends to an event

	$(".add-friends").click(function() {
		$(this).hide();
		$(".add-invite-form").show();
	});

	function invite(){
		$('.add-invite-form-single').submit(function(e) {
			var url = $(this).attr("action");
			$.ajax({
				type: "POST",
				url: url,
				data: $(this).serialize(),
				success: function(data) {
					$('.empty-list').hide();
					$('.search-title').hide();
					$('.user-results').hide();
					$('.invites ul.invite-list').append("<li class='invited-user'><a href='/user/" + data.id + "'>" + data.fname + " " + data.lname + " - Pending</a></li>");
					$('.add-friends').show();
					$('.add-invite-form').hide();
					flashResult("Invitation sent to " + data.fname);
				}
			});
			e.preventDefault();
		});
	}

	$('.add-invite-form').submit(function (e) {
		var url = $(this).attr("action");
		$.ajax({
			type: "POST",
			url: url,
			data: $('.add-invite-form').serialize(),
			success: function(data) {
				$('.search-title').hide();
				$('.user-results').hide();
				if(typeof data == "string"){
					$('#flash-container').html("<ul class='flash-list'><li class='flash-item'>" + data + "</li></ul>");
					$('.flash-list').delay(1500).slideUp();
					$(".error-container").empty();
				} else if (data[0] == "error") {
					validationErrors(data[1], false);
				} else if (data[0] == "multiple results"){
					var results = "<h3 class='section-title search-title'>Search Results</h3><ul class='user-results'>";
					for (i = 0; i < data[1].length; i++){
						results += "<li class='search-result'><a class='link-2' href='/user/" + data[1][i].id + "'>" + data[1][i].fname + " " + data[1][i].lname + "</a><form class='add-invite-form-single' action='/add_invite_single/" + data[2] + "/" + data[3] + "/" + data[1][i].id + "/' method='post'><button type='submit' class='button'>Invite</button></form></li>";
					}
					results += "</ul>";
					$('.add-friends').before(results);
					$('.add-friends').show();
					$('.add-invite-form').hide();
				} else if (data[0] == "success"){
					$('.empty-list').hide();
					$('.invites ul.invite-list').append("<li class='invited-user'><a href='/user/" + data[1].id + "'>" + data[1].fname + " " + data[1].lname + " - Pending</a></li>");
					$('.add-friends').show();
					$('.add-invite-form').hide();
					flashResult("Invitation sent to " + data[1].fname);
				}
				$(".add-invite-form input[type='text']").val('');
				invite();
			}
		});
		e.preventDefault();
	});
});