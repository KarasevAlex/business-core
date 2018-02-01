$(document).ready(function () { 
	$('.js-start').click(function(e){
		var start = $(e.currentTarget);
		var stop = start.next('.js-stop');
		var id = start.parents('.period').data('id');

		$.ajax({
			url: '/period/status',
			method: 'post',
			data: {
				id: id,
				isActive: true
			},
			error: function(){

			}, 
			success: function(data){
				start.prop('disabled', true);
				stop.prop('disabled', false);
			}
		});
	})
	$('.js-stop').click(function(e){
		var stop = $(e.currentTarget);
		var start = stop.prev('.js-start');
		var id = start.parents('.period').data('id');

		$.ajax({
			url: '/period/status',
			method: 'post',
			data: {
				id: id,
				isActive: false
			},
			error: function(){

			},
			success: function(data){
				stop.prop('disabled', true);
				start.prop('disabled', 	false);
			}
		});
	});

	function parseData(str){
	    var arr = str.split(':');
		var endtime = new Date();
		endtime.setHours(arr[0]);
		endtime.setMinutes(arr[1]);
		endtime.setSeconds(arr[2]);
		return endtime;
	}

	$('.period__form').each(function(i, el){
		var period = $(el);
		var prev_period = null;
		if(i != 0)
		    prev_period = $($('.period__form')[i-1]).find('.js-finish-time');

		var begin = period.find('.js-begin-time');
		var duration = period.find('.js-duration-time');
		var finish = period.find('.js-finish-time');
		var is_duration = period.find('.js-is-duration-time');
		var is_finish = period.find('.js-is-finish-time');

		var begin_time = moment(begin.data('value'));
		var duration_time = moment(duration.data('value'));
		var finish_time = moment(finish.data('value'));

		function timeToStr(hours, minutes){
			if(hours < 10)
				hours = '0' + hours;
			if(minutes < 10)
				minutes = '0' + minutes;
			return hours + ':' + minutes;
		}

		function getFinish(){
			var d = duration.val();
			d = d.split(':');

			var b = begin.val();
			b = b.split(':');

			var result_mins = +b[1] + (+d[1]);
			var result_hours = +b[0] + +(d[0]);

			result_hours += Math.floor(result_mins / 60);
			result_mins = result_mins % 60;

			if(result_hours >= 24)
				result_hours -= 24;

			var result = timeToStr(result_hours, result_mins);

			finish.val(result);
		}
		function getDuration(){
			var f = finish.val();
			f = f.split(':');

			var b = begin.val();
			b = b.split(':');

			var result_mins = f[1] - b[1] ;
			var result_hours = f[0] - b[0];

			if(result_mins < 0){
				result_hours--;
				result_mins += 60;
			}
			if (result_hours < 0)
                result_hours -= 24;
			var result = timeToStr(result_hours, result_mins);

			duration.val(result);
		}

		begin.change(function(e){
		    if(parseData(prev_period.val()) > parseData(begin.val()))
		        begin.val(prev_period.val());

			if(is_duration.prop('checked')){
				getFinish()
			} else {
				getDuration();
			}
		});
		duration.blur(function(e){
			getFinish()
		});
		finish.blur(function(e){
			getDuration();

		});
		is_duration.click(function(e){
			finish.prop('readonly', true);
			duration.prop('readonly', false);
		});
		is_finish.click(function(e){
			duration.prop('readonly', true);
			finish.prop('readonly', false);
		});
		period.submit(function(e){
			var d = duration.val();
			var f = finish.val();
			var b = begin.val();

			if(!b || !f || ! d){
				e.preventDefault();
				period
					.append('<p class="error">Неверно заполнены поля</p>');
			}
		});
	});
});