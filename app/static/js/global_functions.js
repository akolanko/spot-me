//Flash result

function flashResult(result) {
	$('#flash-container').html("<ul class='flash-list'><li class='flash-item'>" + result + "</li></ul>");
	$('.flash-list').delay(1500).slideUp();
}


//Show validation errors on form submission

function validationErrors(errors, parent){
	$(".error-container").empty();
	for (var key in errors){
		var value = errors[key];
		if (value.length > 0) {
			var err;
			if (parent === true){
				err = $("#"+key).parent().siblings(".error-container");
			} else{
				err = $("#"+key).next();
			}
			err.html("<div class='validation-error'>" + value + "</div>");
		}
	}
}


//Format date and time objects

function formatDate(date) {
	var monthNames = [
		"January", "February", "March",
		"April", "May", "June", "July",
		"August", "September", "October",
		"November", "December"
	];

	var day = date.getUTCDate();
	var monthIndex = date.getMonth();
	var year = date.getFullYear();

	return monthNames[monthIndex] + ' ' + day + ', ' + year;
}

function formatTime(time) {
	values=time.split(':');
	var hours = parseInt(values[0]);
	var minutes = values[1];
	var am = "AM";
	if (hours > 11 && hours < 24){
		am = "PM";
	}
	if (hours > 12){
		hours = hours - 12;
	}
	return hours + ":" + minutes + " " + am;
}


//Updating form data

function updateData(data){
	for (var key in data){
		var value;
		if (key == 'date' || key == 'birthday'){
			var date = new Date(data[key]);
			value = formatDate(date);
		} else if (key == 'start_time' || key == 'end_time') {
			value = formatTime(data[key]);
		} else {
			value = data[key];
		}
		$("#"+key+"-main").html(value);
	}
}