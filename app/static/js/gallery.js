$(document).ready(function(){
	var photo_delete = [];

	$('.photo img').click(function(e){
		var slideNum = $(e.currentTarget).parent('.photo').data('slick-index');
        $('.modal-photo').addClass('open');
        $('html').addClass('notscroll');
        $('.modal-photo__list').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            autoplay: false,
            arrows: true,
            infinite: true,
            prevArrow : '<span class="glyphicon glyphicon-chevron-left"></span>',
            nextArrow : '<span class="glyphicon glyphicon-chevron-right"></span>'
        });
        $('.modal-photo__list').slick('slickGoTo', slideNum, true);
	});
	$('.js-close-modal').click(function(){
		$('.modal-photo').removeClass('open');
		$('html').removeClass('notscroll');
	});

	$('.js-delete-photo').click(function(e){
		var photo_el = $(e.currentTarget).parents('.photo');
		var photo_id = photo_el.data('photo-id');

		if(photo_delete.indexOf(photo_id) === -1){
			photo_delete.push(photo_id);
			$('.photo[data-photo-id=' + photo_id + ']').each(function(index, domElement){
				$(domElement).addClass('deleted');
			});
		}
	});

	$('.reestablish .btn').click(function(e){
		var photo_el = $(e.currentTarget).parents('.photo');
		var photo_id = photo_el.data('photo-id');
		var i = photo_delete.indexOf(photo_id);
		if(i !== -1){
			delete photo_delete[i];
			$('.photo[data-photo-id=' + photo_id + ']').each(function(index, domElement){
				$(domElement).removeClass('deleted');
			});
		}
	});

	window.onbeforeunload = function() {
		$.ajax({
			url: '/gallaries/photo/delete',
			method: 'post',
			data: {
				delete: photo_delete
			}
		})
	};

	$('.js-main-photo').click(function(e){
		var photo_id = $(e.currentTarget).parents('.photo').data('photo-id');

		$.ajax({
			url: '/gallery/poster',
			method: 'post',
			data: {
				id: photo_id
			},
			success: function(data){
				$('.photo.main').removeClass('main');
				$('.photo.main').removeAttr('disabled');
				$('.photo[data-photo-id=' + photo_id + ']').each(function(index, domElement){
					$(domElement).addClass('main');
					$(domElement).attr('disabled','disabled');
				});
			},
			error: function(err) {

			}
		});
	});
	
});