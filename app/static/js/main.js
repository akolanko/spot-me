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

		$.post("/add_friend",
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
		var friend = $(this).closest("li");

		formInput = {
			"friend_id": $(this).find('input[name="user_id"]').data("friend")
		};

		$.post("/unfriend",
			formInput,
			function() {
				friend.hide();
				updateConnectionCount();
			}
		);

		e.preventDefault();
	});


	//Accepting friends

	$("#accept-friend-form").submit(function(e) {
		e.preventDefault();

		var formInput = {
			"user_id_2": $("#user-info").data("userid")
		};

		$.post("/accept_friend",
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

		$.post("/accept_friend",
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

		$.post("/delete_friend_request",
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

				$.post("/new_message",
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
			var day = (result[2][0].timestamp);
			html += "<div class='message-date'>" + day + "</div>";
			for (i = 0; i < result[2].length; i++) {
				if (day != result[2][i].timestamp) {
					html += "<div class='message-date'>" + result[2][i].timestamp + "</div>";
					day = result[2][i].timestamp;
				}
				html += "<div class='message-outer'>";
				if (result[2][i].sender == result[3].id) {
					html += "<div class='message message-1'>";
				} else {
					html += "<div class='message message-2'>";
				}
				html += result[2][i].body + "<div class='clear'></div></div>";
			}
		}
		$(".conversation-messages").html(html);
	}


	//Create new conversation

	$('#new-conversation').submit(function(e) {
		var username = $("#new-conversation-input").val();

		formInput = {
			"username": username
		};

		$.post("/create_new_conversation",
			formInput,
			function(result) {
				if(typeof result == "string"){
					$("#new-conversation-input").val('');
					flashResult(result);
				} else {
					$(".friend-search").hide();
					$("#conversation-messages-2").removeAttr("id");
					$(".compose-message").html("<form id='new-message' action='/new_message' method='post'><input type='hidden' id='conversation-id' data-conversation='" + result[0].id + "'><textarea name='body' id='new-message-body' placeholder='Write a message...'></textarea><button type='submit' class='hidden'></button></form>");
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

		$.post("/search_discover",
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
});