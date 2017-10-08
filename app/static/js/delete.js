function deleteItem(modal){
		var $item;
		modal.on('show.bs.modal', function (e) {
			var $btn = $(e.relatedTarget);
			$item = $btn.parent('.js-item');
		  	var $nameText = modal.find('#item-name-text');
		  	var $idText = modal.find('#item-id-text');
		  	var $input = modal.find('#item-id-input');

		  	$nameText.text($btn.data('item-name'));
		  	$idText.text($btn.data('item-id'));
		  	$input.val($btn.data('item-id'));
		})
		modal.on('hide.bs.modal', function(e){
			var $input = modal.find('#item-id-input').val('');
		})
		modal.find('form').on('submit', function(e){
			e.preventDefault();
			var url = $(e.currentTarget).attr('action');
			var data = $(e.currentTarget).find('#item-id-input').val();
			$.ajax({
				url: url,
				method: 'post',
				data: {
					id: data
				},
				success: function(){
					$item.remove();
				},
				error: function(){
					console.log('error');
				}
			});
		})
	}