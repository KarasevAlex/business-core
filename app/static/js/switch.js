$(document).ready(function () { 
	var full_time_format = 'gggg-MM-DD HH:mm';
	var time_format = 'HH:mm';
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
				document.location.reload();
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
		var duration_time = moment(duration.data('value'), time_format);
		var finish_time = moment(finish.data('value'));

		begin.val(begin_time.format(full_time_format));
		duration.val(duration_time.format(time_format));
		finish.val(finish_time.format(full_time_format));

		function getFinish(){
			var duration_val =  moment.duration(duration.val(), time_format);

			var begin_val =  moment(begin.val());

			var finish_val = begin_val.add(duration_val);//moment(begin_val + duration_val);

			finish.val(finish_val.format(full_time_format));
		}
		function getDuration(){
			var finish_val = moment(finish.val());

			var begin_val = moment(begin.val());

			var duration_val = finish_val
				.subtract(begin_val.get('hours'), 'hours')
				.subtract(begin_val.get('minutes'), 'minutes');
			
			duration.val(duration_val.format(time_format));
		}

		begin.change(function(e){
			var prev = moment(prev_period.val());
			var current = moment(begin.val())
		    if(prev > current)
		        begin.val(prev_period.val());

			if(is_duration.prop('checked')){
				getFinish()
			} else {
				getDuration();
			}
		});
		duration.change(function(e){
			getFinish()
		});
		finish.change(function(e){
			getDuration();

		});
		is_duration.click(function(e){
			finish.prop('disabled', true);
			duration.prop('disabled', false);
		});
		is_finish.click(function(e){
			duration.prop('disabled', true);
			finish.prop('disabled', false);
		});

		if(is_duration.prop('checked'))
			is_duration.trigger('click');
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