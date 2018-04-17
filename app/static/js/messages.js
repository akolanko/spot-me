$(document).ready( function() {

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
			var conversation_id = $("#conversation-id").data("conversation");
			var code = e.keyCode || e.which;
			if (code == 13) {
				var body = $("#new-message-body").val();

				formInput = {
					"conversation_id": conversation_id,
					"body": body
				};

				$.post("/new_message/",
					formInput,
					function() {
						var target = "#conversation-" + conversation_id + " .recent-msg";
						$('.conversation-messages').append("<div class='message-outer'><div class='message message-1'>" + body + "</div><div class='clear'></div></div>");
						$('.conversation-messages').scrollTop($('.conversation-messages')[0].scrollHeight);
						$(target).html(body);
					}
				);

				$("#new-message-body").val('');
			}
		});
	}

	sendMessage();


	//Append all messages to a conversation

	function appendMessages(data) {
		html = "";
		if (data["messages"][0]) {
			var date = new Date(data["messages"][0].timestamp);
			html += "<div class='message-date'>" + date.getMonth() + "/" + date.getDay() + "/" + date.getFullYear() + "</div>";
			for (i = 0; i < data["messages"].length; i++) {
				var msgDate = new Date(data["messages"][i].timestamp);
				if (date.getDay() != msgDate.getDay()) {
					html += "<div class='message-date'>" + msgDate.getMonth() + "/" + msgDate.getDay() + "/" + msgDate.getFullYear() + "</div>";
					date = msgDate;
				}
				html += "<div class='message-outer'>";
				if (data["messages"][i].sender == data["current_user"].id) {
					html += "<div class='message message-1'>";
				} else {
					html += "<div class='message message-2'>";
				}
				html += data["messages"][i].body + "</div><div class='clear'></div>";
			}
		}
		$(".conversation-messages").html(html);
	}


	//New event - messages page

	$('#new-event-form .event-field').click(function(){
		$(this).find("input").focus();
	});

	function newEvent() {

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
	}
	newEvent();


	//Show conversation details on conversation creation

	function showMessageDetails(data){
		$(".friend-search").hide();
		$("#conversation-messages-2").removeAttr("id");
		$(".compose-message").html("<form id='new-message' action='/new_message/' method='post'><input type='hidden' id='conversation-id' data-conversation='" + data["conversation"].id + "'><textarea name='body' id='new-message-body' placeholder='Write a message...'></textarea><button type='submit' class='hidden'></button></form>");
		$(".friend-details").html("<div id='user_id' data-userid='" + data["friend"].id + "'></div><a href='/user/" + data["friend"].id + "'><div class='left friend-thumb'><img src='" + data["friend"].avatar + "' /></div></a><div class='right'><div class='name'>" + data["friend"].fname + "</div></div>");
		$(".new-event").show();
		$(".sidebar .outer").removeClass("no-border");
		newEvent();
	}


	//Show a new conversation in the user's list of conversations

	function showConversationInList(data){
		$("#conversation-list").prepend("<a class='link-2' href='/conversation/" + data["conversation"].id + "'><li id='conversation-" + data["conversation"].id + "'><div class='left friend-thumb'><img src='" + data["friend"].avatar + "'/></div><div class='right'><div class='name'>" + data["friend"].fname + "</div><div class='recent-msg'></div></div></li></a>");
	}


	//Create new conversation from search result list

	function postSingle() {
		$('.create-conversation-form-single').submit(function(e) {
			var url = $(this).attr("action");
			$.ajax({
				type: "POST",
				url: url,
				data: $(this).serialize(),
				success: function(data) {
					if (data["status"] == "error") {
						$("#new-conversation-input").val('');
						flashResult(data["results"]);
					} else if (data["status"] == "conversation exists") {
						showMessageDetails(data);
						appendMessages(data);
						messageScroll();
						sendMessage();
					} else if (data["status"] == "new conversation") {
						showMessageDetails(data);
						showConversationInList(data);
						sendMessage();
					}
				}
			});
			e.preventDefault();
		});
	}


	//Create new conversation from search form

	$('#new-conversation').submit(function(e) {
		var name = $("#new-conversation-input").val();

		formInput = {
			"name": name
		};

		$.post("/create_new_conversation/",
			formInput,
			function(data) {
				if (data["status"] == "none" || data["status"] == "error"){
					$("#new-conversation-input").val('');
					flashResult(data["results"]);
				} else if (data["status"] == "conversation exists"){
					showMessageDetails(data);
					appendMessages(data);
					messageScroll();
					sendMessage();
				} else if (data["status"] == "new conversation"){
					showMessageDetails(data);
					showConversationInList(data);
					sendMessage();
				} else if (data["status"] == "multiple"){
					var html = "<div class='search-drop-down'><ul>";
					for (var i = 0; i < data["results"].length; i++){
						html += "<li><form class='create-conversation-form-single' action='/post_conversation_single/" + data["results"][i].id + "/' method='post'><button type='submit' class='non-btn'>" + data["results"][i].fname + " " + data["results"][i].lname + "</button></form></li>";
					}
					html += "</ul></div>";
					$(".friend-search").append(html);
					postSingle();
				}
			}
		);
		e.preventDefault();
	});
});