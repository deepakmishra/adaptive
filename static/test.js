var remaining_time_in_seconds;
var timer;

$(document).ready(function() {

	$(".start-test").click(function() {
		var email = $(".email-box").val();
		if (!email) {
			return;
		}
		$.post("api/users/search", {
				email: email
			})
			.done(function(data) {
				if (!data['eligible']) {
					if (data['last_test'] && data['last_test']['score']) {
						var date_str = new Date(data['last_test']['expiry_time']).toGMTString();
						var obj = $(".not-eligible").text($(".not-eligible").text() + "\n\nLast Score : " + data['last_test']['score'] + "\n\nExpiry Date : " + date_str);
						obj.html(obj.html().replace(/\n/g, '<br/>'));
						if (data['last_test']['analytics']) {
							analytics(data['last_test']['analytics']);
						}
					}
					$(".first-page").hide();
					$(".not-eligible").show();
				} else {
					$('input[name=user_id]').val(data['id']);
					$(".candidate-name").text(data['email']);

					$.post("api/users/" + $('input[name=user_id]').val() + "/tests")
						.done(populate_question);
				}
			});
	});

	$(".test-submit-button").click(function() {
		var selected_answer = $('input[name=selected_answer]:checked').val();
		if (selected_answer) {
			$.post("api/users/" + $('input[name=user_id]').val() + "/attempts", {"answer_id": selected_answer})
				.done(populate_question);
		}
	});

	$(".test-end").click(function() {
		$.post("api/users/" + $('input[name=user_id]').val() + "/attempts", {"answer_id": 0})
			.done(populate_question);
	});


});

function set_option_clicks() {
	$(".test-answer").click(function() {
		$(".objective-selected").removeClass("objective-selected");
		$(".option-selected").removeClass("option-selected");
		$("input.objective-radio").removeAttr('checked');
		$(this).find(".objective-virtual-radio").addClass("objective-selected");
		$(this).find("input.objective-radio").attr('checked', 'checked');
		$(this).addClass("option-selected");
	});

}

function clear_timer() {
	if (timer) {
		clearInterval(timer);
		timer = null;
	}
}

function start_timer() {
	clear_timer();
	timer = setInterval(function() {
		$(".test-timer").text(format_seconds_to_time(remaining_time_in_seconds));
		remaining_time_in_seconds = remaining_time_in_seconds - 1;
	}, 1000);
}

function format_seconds_to_time(seconds) {
	var date = new Date(null);
	date.setSeconds(seconds);
	return date.toISOString().substr(11, 8);
}

var populate_question = function(data) {
	$(".test-ended-score-ph").text(data['test_score']);
	if (!data['question_number']) {
		$(".test-ended").show();
		$(".test-wrapper").hide();
		clear_timer();
		if (data['analytics']) {
			analytics(data['analytics']);
		}
		return;
	}

	remaining_time_in_seconds = data['remaining_time_in_seconds'];
	start_timer();

	$(".test-score-ph").text(data['test_score']);
	$(".test-question-number-ph").text(data['question_number']);
	
	$(".test-question").html(data['text']);
	var option_list = $(".test-answer-list");
	option_list.html("");

	$.each(data['answers'], function(i) {
		var answer = data['answers'][i];
		var li = $('<li/>')
			.appendTo(option_list);
		var answer_div = $('<div/>')
			.addClass('test-answer')
			.appendTo(li);
		$('<div/>').addClass('objective-virtual-radio')
			.appendTo(answer_div);
		$('<input>').addClass('objective-radio')
			.attr('type', 'radio').attr('name', 'selected_answer')
			.attr('value', answer['id']).attr('id', answer['id'])
			.appendTo(answer_div);
		var span = $('<span/>').addClass('test-answer-text')
			.appendTo(answer_div);

		if (!answer['text']) {
			answer['text'] = "&nbsp;&nbsp;";
		}

		span.html(answer['text']);

		set_option_clicks();

	});

	$(".first-page").hide();
	$(".test-wrapper").show();
	$("#test-analytics").hide();
}

function analytics(analytics_data) {

	data_points = []
	analytics_data.forEach(function(a){data_points.push(a.score);});

	$("#test-analytics").show();

	Highcharts.chart('test-analytics', {

		title: {
			text: 'Performance over the test'
		},
		subtitle: {
			text: 'Breaking Point'
		},
		yAxis: {
			title: {
				text: 'Test Score'
			}
		},
		legend: {
			layout: 'vertical',
			align: 'right',
			verticalAlign: 'middle'
		},
		plotOptions: {
			series: {
				label: {
					connectorAllowed: false
				},
				pointStart: 0
			}
		},
		series: [{
			name: 'Score',
			data: data_points
		}],
		responsive: {
			rules: [{
				condition: {
					maxWidth: 500
				},
				chartOptions: {
					legend: {
						layout: 'horizontal',
						align: 'center',
						verticalAlign: 'bottom'
					}
				}
			}]
		}
	});
}


