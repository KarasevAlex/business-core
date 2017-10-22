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
				start.attr('disabled', 'disabled');
				stop.attr('disabled', false);
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
				stop.attr('disabled', 'disabled');
				start.attr('disabled', 	false);
			}
		});
	})
});