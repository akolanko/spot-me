$(document).ready( function() {

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
	

	// Messenger scroll

	$('.conversation-messages').scrollTop($('.conversation-messages')[0].scrollHeight);


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


	//Send new message

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
				}
			);

			$("#new-message-body").val('');
		}
	});

});