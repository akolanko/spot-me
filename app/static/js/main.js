$(document).ready( function() {

	//Hide flash

	$('.flash-list').delay(1500).slideUp();


	//Flash result

	function flashResult(result) {
		$('#flash-container').html("<ul class='flash-list'><li class='flash-item'>" + result + "</li></ul>");
		$('.flash-list').delay(1500).slideUp();
	}


	//Navigation menu

	$('.notification-overlay').click(function(){
		var id = $(this).parent().attr('id');
		$(".drop-down:not(#" + id + " .drop-down)").hide();
		$(this).siblings('.drop-down').slideToggle(500);
		$('#menu-line-2').removeClass('active');
		$('#menu-line-1').removeClass('active');
		$('#menu-line-3').removeClass('active');
	});

	$('#menu-btn').click(function(){
		$(".drop-down:not(#drop-down-menu)").hide();
		$('#drop-down-menu').slideToggle(500);
		$('#menu-line-2').toggleClass('active');
		$('#menu-line-1').toggleClass('active');
		$('#menu-line-3').toggleClass('active');
	});


	//Adding friends

	$("#add-friend-form").submit(function(e) {
		e.preventDefault();

		var formInput = {
			"user_id_2": $("#user-info").data("userid")
		};

		$.post("/add_friend/",
			formInput,
			function() {
				$("#connect-btn").html("<button class='button button-2 disabled'>Pending</button>");
			}
		);
	});


	//Update friend notification count

	function updateFriendRequestCount(){
		var count = parseInt($('#friend-request-count').html());
		count = count - 1;
		if (count === 0) {
			$('#friend-request-count').hide();
		} else {
			$('#friend-request-count').html(count);
		}
	}


	//Unfriending

	$(".unfriend-form").submit(function(e) {

		if (window.confirm("Are you sure you want to unfriend this user?")) {

			var friend = $(this).closest("li");

			formInput = {
				"friend_id": $(this).find('input[name="user_id"]').data("friend")
			};

			$.post("/unfriend/",
				formInput,
				function() {
					friend.hide();
					updateConnectionCount();
				}
			);
		}

		e.preventDefault();
	});


	//Accepting friends

	$("#accept-friend-form").submit(function(e) {
		e.preventDefault();

		var formInput = {
			"user_id_2": $("#user-info").data("userid")
		};

		$.post("/accept_friend/",
			formInput,
			function() {
				$("#connect-btn").html("<button class='button button-2 disabled'>Friends</button>");
				updateFriendRequestCount();
			}
		);
	});


	$(".accept-friend-notification").submit(function(e) {
		var friend = $(this).closest("li");

		formInput = {
			"user_id_2": $(this).find('input[name="friend_id"]').data("friend")
		};

		$.post("/accept_friend/",
			formInput,
			function() {
				friend.hide();
				updateFriendRequestCount();
			}
		);

		e.preventDefault();
	});


	//Deleting friend requests

	$(".delete-friend-request-form").submit(function(e) {
		var friend = $(this).closest("li");

		formInput = {
			"user_id_2": $(this).find('input[name="friend_id"]').data("friend")
		};

		$.post("/delete_friend_request/",
			formInput,
			function() {
				friend.hide();
				updateFriendRequestCount();
			}
		);

		e.preventDefault();
	});


	// Messenger scroll

	function messageScroll() {
		var elementExists = $(".conversation-messages").length > 0;
		if (elementExists){
			$('.conversation-messages').scrollTop($('.conversation-messages')[0].scrollHeight);
		}
	}

	messageScroll();


	//Send new message

	function sendMessage() {
		$('#new-message-body').keypress(function(e) {
			var code = e.keyCode || e.which;
			if (code == 13) {
				var body = $("#new-message-body").val();

				formInput = {
					"conversation_id": $("#conversation-id").data("conversation"),
					"body": body
				};

				$.post("/new_message/",
					formInput,
					function() {
						$('.conversation-messages').append("<div class='message-outer'><div class='message message-1'>" + body + "</div><div class='clear'></div></div>");
						$('.conversation-messages').scrollTop($('.conversation-messages')[0].scrollHeight);
					}
				);

				$("#new-message-body").val('');
			}
		});
	}

	sendMessage();


	//Append all messages to a conversation

	function appendMessages(result) {
		html = "";
		if (result[2][0]) {
			var date = new Date(result[2][0].timestamp);
			html += "<div class='message-date'>" + date.getMonth() + "/" + date.getDay() + "/" + date.getFullYear() + "</div>";
			for (i = 0; i < result[2].length; i++) {
				var msgDate = new Date(result[2][i].timestamp);
				if (date.getDay() != msgDate.getDay()) {
					html += "<div class='message-date'>" + msgDate.getMonth() + "/" + msgDate.getDay() + "/" + msgDate.getFullYear() + "</div>";
					date = msgDate;
				}
				html += "<div class='message-outer'>";
				if (result[2][i].sender == result[3].id) {
					html += "<div class='message message-1'>";
				} else {
					html += "<div class='message message-2'>";
				}
				html += result[2][i].body + "</div><div class='clear'></div>";
			}
		}
		$(".conversation-messages").html(html);
	}


	//Create new conversation

	$('#new-conversation').submit(function(e) {
		var username = $("#new-conversation-input").val().toLowerCase();

		formInput = {
			"username": username
		};

		$.post("/create_new_conversation/",
			formInput,
			function(result) {
				if(typeof result == "string"){
					$("#new-conversation-input").val('');
					flashResult(result);
				} else {
					$(".friend-search").hide();
					$("#conversation-messages-2").removeAttr("id");
					$(".compose-message").html("<form id='new-message' action='/new_message/' method='post'><input type='hidden' id='conversation-id' data-conversation='" + result[0].id + "'><textarea name='body' id='new-message-body' placeholder='Write a message...'></textarea><button type='submit' class='hidden'></button></form>");
					$(".friend-details").html("<a href='/user/" + result[1].id + "'><div class='left friend-thumb'><img src='" + result[1].avatar + "' /></div></a><div class='right'><div class='name'>" + result[1].fname + "</div></div>");

					if (result.length == 4) {
						appendMessages(result);
						messageScroll();
					}
					sendMessage();
				}
			}
		);

		e.preventDefault();
	});


	//Discover search

	$("#search-discover").submit(function(e) {
		var interest = $("#search-discover-input").val().toLowerCase();

		formInput = {
			"interest": interest
		};

		$.post("/search_discover/",
			formInput,
			function(result) {
				var html = "";
				$("#search-discover-input").val('');
				if(typeof result == "string"){
					html += "<div class='result'>" + result + "</div>";
				} else{
					for (i = 0; i < result.length; i++) {
						html += "<li><a class='link-2' href='/user/" + result[i][0].id + "'><div class='left'><div class='friend-thumb'><img src=" + result[i][0].avatar + " /></div></div><div class='right'><a class='link-2' href='/user/" + result[i][0].id + "'><div class='friends-name'>" + result[i][0].fname + " " + result[i][0].lname + "</div></a><div class='interests'>Interests: ";
						for (j = 0; j < result[i][1].length; j++) {
							if (j > 0) {
								html += ", ";
							}
							html += "<span class='lowercase'>" + result[i][1][j].name + "</span>";
						}
						html += "</div></div></a></li>";
					}
				}
				$(".users ul").html(html);
			}
		);

		e.preventDefault();
	});


	//Show validation errors

	function validationErrors(errors, parent){
		for (var key in errors){
			var value = errors[key];
			if (value.length > 0) {
				var err;
				if (parent === true){
					err = $("#"+key).parent().siblings(".error-container");
				} else{
					err = $("#"+key).next();
				}
				err.html("<div class='validation-error'>" + value + "</div>");
			}
		}
	}


	//Format date and time objects

	function formatDate(date) {
		var monthNames = [
			"January", "February", "March",
			"April", "May", "June", "July",
			"August", "September", "October",
			"November", "December"
		];

		var day = date.getUTCDate();
		var monthIndex = date.getMonth();
		var year = date.getFullYear();

		return monthNames[monthIndex] + ' ' + day + ', ' + year;
	}

	function formatTime(time) {
		values=time.split(':');
		var hours = parseInt(values[0]);
		var minutes = values[1];
		var am = "AM";
		if (hours > 11 && hours < 24){
			am = "PM";
		}
		if (hours > 12){
			hours = hours - 12;
		}
		return hours + ":" + minutes + " " + am;
	}


	//Updating form data

	function updateData(data){
		for (var key in data){
			var value;
			if (key == 'date' || key == 'birthday'){
				var date = new Date(data[key]);
				value = formatDate(date);
			} else if (key == 'start_time' || key == 'end_time') {
				value = formatTime(data[key]);
			} else {
				value = data[key];
			}
			$("#"+key+"-main").html(value);
		}
	}


	//Account Update

	$('#edit-account-btn').click(function(){
		$('#account-main').hide();
		$('#account-btns-main').hide();
		$('#account-form').show();
		$('#account-update-btn').show();
		$('#acc-update-del-btn').show();
	});

	$('#update-account-form').submit(function (e) {
		var url = "/update_account/";
		$.ajax({
			type: "POST",
			url: url,
			data: $('#update-account-form').serialize(),
			success: function(data) {
				if (data[0] == "error") {
					validationErrors(data[1], true);
					if (data[2] !== false){
						validationErrors(data[2], true);
					}
				} else {
					$(".error-container").empty();
					$('#account-form').hide();
					$('#account-main').show();
					$('#account-update-btn').hide();
					$('#acc-update-del-btn').hide();
					$('#account-btns-main').show();
					updateData(data[1]);
				}
			}
		});
		e.preventDefault();
	});


	//Password Update

	$('#update-password-form').submit(function (e) {
		var url = "/update_password/";
		$.ajax({
			type: "POST",
			url: url,
			data: $('#update-password-form').serialize(),
			success: function(data) {
				if(typeof data == "string"){
					$('#flash-container').html("<ul class='flash-list'><li class='flash-item'>" + data + "</li></ul>");
					$('.flash-list').delay(1500).slideUp();
					$("#update-password-form input[type='password']").val('');
					$(".error-container").empty();
				} else {
					validationErrors(data, false);
				}
			}
		});
		e.preventDefault();
	});


	//New event - messages page

	$('#new-event-form .event-field').click(function(){
		$(this).find("input").focus();
	});

	$('#new-event-form').submit(function (e) {
		var user_id = $("#user_id").data("userid");
		var url = "/new_event/" + user_id + "/";
		$.ajax({
			type: "POST",
			url: url,
			data: $('#new-event-form').serialize(),
			success: function(data) {
				if(typeof data == "string"){
					flashResult(data);
					$(".error-container").empty();
					$('input[type="text"]').val('');
					$('input[type="date"]').val('');
					$('input[type="time"]').val('');
					$('textarea').val('');
				} else {
					validationErrors(data, true);
				}
			}
		});
		e.preventDefault();
	});


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
				$('.invites').html(html);

				btns = "<div class='event-buttons inline-buttons' id='event-btns-main'><button class='button button-1' id='edit-event-btn'>Edit</button><form onsubmit='return confirm(\"Are you sure you want to remove yourself from this event?\");' class='remove-event-form' action='remove_event/'" + user_event_id + " method='post'><button type='submit' class='button button-4'>Remove</button></form></div>";
				$(".event-info").append(btns);

				if( $('#invite-list').height() === 0 ) {
					$('#invite-list').html("<div class='no-results'>You do not currently have any event invitations.</div>");
				}
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


	//Updating an event

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
});
