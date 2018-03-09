// $(document).ready( function() {
//   function showSentRequest(result) {
//       $("#connect-btn").html(result).attr("disabled", true);
//   }

//   function sendFriendRequest(evt) {
//       evt.preventDefault();

//       var formInput = $("#user-info").data("userid");

//       $.post("/add_friend",
//              formInput,
//              showSentRequest
//              );
//   }

//   $("#add-friend-form").on("submit", sendFriendRequest);
// });