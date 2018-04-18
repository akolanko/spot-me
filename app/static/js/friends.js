$(document).ready( function() {
	//Adding friends

	$("#add-friend-form").submit(function(e) {
		e.preventDefault();

		var action = $(this).attr("action");

		$.post(action,
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


	//Update connection count on profile page when unfriending

	function updateConnectionCount(){
		arr = $('.connections-count a').html().split(' ');
		count = parseInt(arr[0]);
		count -= 1;
		if (count == 1){
			$('.connections-count a').html(count + " connection");
		} else {
			$('.connections-count a').html(count + " connections");
		}
	}


	//Unfriending

	$(".unfriend-form").submit(function(e) {

		if (window.confirm("Are you sure you want to unfriend this user?")) {

			var friend = $(this).closest("li");
			var friend_id = $(this).find('input[name="user_id"]').data("friend");
			var friend_thumb = $(".friend-thumb[data-userid='" + friend_id + "']");

			formInput = {
				"friend_id": friend_id
			};

			$.post("/unfriend/",
				formInput,
				function() {
					friend.hide();
					updateConnectionCount();
					friend_thumb.parent().hide();
				}
			);
		}

		e.preventDefault();
	});


	//Accepting friends

	$("#accept-friend-form").submit(function(e) {
		e.preventDefault();

		var action = $(this).attr("action");

		$.post(action,
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