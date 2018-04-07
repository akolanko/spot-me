$(document).ready( function() {
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
});