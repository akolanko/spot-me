$(document).ready( function() {

	$('.nav-item').click(function(){
		$(this).find('.drop-down').slideToggle(500);
	});


	//Adding friends

	function updateButton(result) {
		$("#connect-btn").html("<button class='button button-2 disabled'>Pending</button>");
	}

	function sendFriendRequest(e) {
		e.preventDefault();

		var formInput = {
			"user_id_2": $("#user-info").data("userid")
		};

		$.post("/add_friend",
			formInput,
			updateButton
		);
	}

	$("#add-friend-form").on("submit", sendFriendRequest);


	//Unfriending


	$(".unfriend-form").submit(function(e) {

		var friend = $(this).closest("li");

		formInput = {
			"friend_id": $(this).find('input[name="user_id"]').data("friend")
		};

		$.post("/unfriend",
			formInput,
			function() {
				friend.fadeOut();
			}
		);

		e.preventDefault();

	});


	//Accepting friends

	function updateBtn(result) {
		$("#connect-btn").html("<button class='button button-2 disabled'>Friends</button>");
	}

	function acceptFriendRequest(e) {
		e.preventDefault();

		var formInput = {
			"user_id_2": $("#user-info").data("userid")
		};

		$.post("/accept_friend",
			formInput,
			updateBtn
		);
	}

	$("#accept-friend-form").on("submit", acceptFriendRequest);

	$(".accept-friend-notification").submit(function(e) {

		var friend = $(this).closest("li");

		formInput = {
			"user_id_2": $(this).find('input[name="friend_id"]').data("friend")
		};

		$.post("/accept_friend",
			formInput,
			function() {
				friend.fadeOut();
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
				friend.fadeOut();
			}
		);

		e.preventDefault();

	});
});