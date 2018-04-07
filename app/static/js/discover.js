$(document).ready( function() {
	
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
});