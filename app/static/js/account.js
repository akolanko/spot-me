$(document).ready( function() {
	
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
});