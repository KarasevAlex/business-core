function deleteItem(modal, delete_url){
		var $item;
		var id;
		$('.js-delete-modal').on('show.bs.modal', function (e) {
			var $btn = $(e.relatedTarget);
			console.log($btn)
			$item = $btn.parents('.js-item');
			console.log($item)
		  	var $nameText = modal.find('#item-name-text');
		  	var $idText = modal.find('#item-id-text');

		  	$nameText.text($btn.data('item-name'));
		  	$idText.text($btn.data('item-id'));
		  	id = $btn.data('item-id');
		})
		modal.find('form').on('submit', function(e){
			e.preventDefault();
			var url = delete_url + id;
			$.ajax({
				url: url,
				method: 'post',
				success: function(){
					$item.remove();
					modal.modal('hide');
				},
				error: function(){
					console.log('error');
				}
			});
		})
	}

$(document).ready(function(){
	var form = $('#login-form');
	form.on('submit', function(e){
		e.preventDefault();
		var form = $(e.currentTarget);
		form.find('.login-error').addClass('hide');

		$.ajax({
			url: form.attr('action'),
			method: form.attr('method'),
			data: form.serialize(),
			success: function(res){
				document.location.href = res;
			},
			error: function(res){
				form.find('.login-error').removeClass('hide');
			}
		})
	});
	deleteItem($('#deleteGameModal'), '/games/remove/');
	deleteItem($('#deleteAlbumModal'), '/gallery/remove/');
	deleteItem($('#deleteNewsModal'), '/news/remove/');
});