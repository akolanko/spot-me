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

	function updateConnectionCount(increment, user_id, avatar){
		arr = $('.connections-count a').html().split(' ');
		count = parseInt(arr[0]);
		if (increment === true) {
			count += 1;
			if (count < 6) {
				$(".profile-friends ul").append("<li><a href= '/user/" + user_id + "'<div class='friend-thumb' data-userid='" + user_id + "'><img src='" + avatar + "'/></div></a></li>");
			}
		} else {
			count -= 1;
		}
		if (count == 1){
			$('.connections-count a').html(count + " connection");
		} else {
			$('.connections-count a').html(count + " connections");
		}
	}


	//Unfriending

	$(".unfriend-form").submit(function(e) {

		if (window.confirm("Are you sure you want to unfriend this user?")) {
			var action = $(this).attr("action");
			var friend = $(this).closest("li");
			var friend_id = $(this).find('input[name="user_id"]').data("friend");
			var friend_thumb = $(".friend-thumb[data-userid='" + friend_id + "']");

			$.post(action,
				function(data) {
					friend.hide();
					updateConnectionCount(false, data["user"]["id"], data["user"]["avatar"]);
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
			function(data) {
				$("#connect-btn").html("<button class='button button-2 disabled'>Friends</button>");
				updateConnectionCount(true, data["user"]["id"], data["user"]["avatar"]);
				updateFriendRequestCount();
			}
		);
	});


	$(".accept-friend-notification").submit(function(e) {
		var friend = $(this).closest("li");
		var friend_id = $(this).find('input[name="friend_id"]').data("friend");
		var action = $(this).attr("action");
		var pathname = window.location.pathname;

		$.post(action,
			function(data) {
				friend.hide();
				if (pathname == "/user/" + friend_id) {
					$("#connect-btn").html("<button class='button button-2 disabled'>Friends</button>");
					updateConnectionCount(true, data["user"]["id"], data["user"]["avatar"]);
				}
				updateFriendRequestCount();
			}
		);

		e.preventDefault();
	});


	//Deleting friend requests

	$(".delete-friend-request-form").submit(function(e) {
		var friend = $(this).closest("li");
		var action = $(this).attr("action");

		$.post(action,
			function() {
				friend.hide();
				updateFriendRequestCount();
			}
		);

		e.preventDefault();
	});
});