$(document).ready(function(){
	$('.js-down').click(function(e){
		var target = $(e.currentTarget).parents('.js-album');
		var next = target.next('.js-album');
		if(next.length > 0){
			target.detach();
			next.after(target);
			var id = target.data('id');
			$.ajax({
			    url: '/gallery/position/down/' + id,
			    method: 'post',
		        error: function(res){
		            console.log(res);
		        },
		        success: function(res){
		            console.log(res);
		        }
			});
		} else 
			return;
	});
	$('.js-up').click(function(e){
		var target = $(e.currentTarget).parents('.js-album');
		var prev = target.prev('.js-album');
		if(prev.length > 0){
			target.detach();
			prev.before(target);
			var id = target.data('id');
			$.ajax({
			    url: '/gallery/position/up/' + id,
			    method: 'post',
		        error: function(res){
		            console.log(res);
		        },
		        success: function(res){
		            console.log(res);
		        }
			});
		} else 
			return;
	});
});