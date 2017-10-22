$(document).ready(function () {
	var timer = $('.session-panel .js-timer');

	function getTimeRemaining(endtime){
	  var t = Date.parse(endtime) - Date.parse(new Date());
	  var seconds = Math.floor( (t/1000) % 60 );
	  var minutes = Math.floor( (t/1000/60) % 60 );
	  var hours = Math.floor( (t/(1000*60*60)) % 24 );
	  return {
	   'total': t,
	   'hours': hours,
	   'minutes': minutes,
	   'seconds': seconds
  	  };
	}
	function initializeClock(timer){
		var hours = timer.find('.js-hours');
		var minuts = timer.find('.js-minutes');
		var seconds = timer.find('.js-seconds');

		var str = timer.data('finish-time');
		var arr = str.split(':');
		var endtime = new Date();
		endtime.setHours(arr[0]);
		endtime.setMinutes(arr[1]);
		endtime.setSeconds(arr[2]);

		var now = new Date();
		if(now >= endtime)
		    return;

		var timeinterval = setInterval(function(){
			var t = getTimeRemaining(endtime);
			hours.text(('0' + t.hours).slice(-2));
			minuts.text(('0' + t.minutes).slice(-2));
			seconds.text(('0' + t.seconds).slice(-2));
			if(t.total<=0){
			  clearInterval(timeinterval);
			  location.reload();
			}
		},1000);
	}
	if(timer.length > 0)
		initializeClock(timer);

	$('.js-game').each(function(i, el){
		var timer = $(el).find('.js-timer');
		if(timer.length > 0)
			initializeClock(timer);
	});
});