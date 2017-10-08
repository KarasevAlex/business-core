$(document).ready(function(){
	$('#deleteGameModal').modal({show: false});
	deleteItem($('#deleteGameModal'));

	$('#team-number').on('blur', function(e){
		setMarketVolume();
	})
	function getRandomVolume(num){
		var rnd = Math.random();
	  	return Math.round(parseInt((rnd * 250) + 50) * 0.33) * num;
	}
	function Amount(val){
		this.val = val;
		this.isError = false;
	}
	var formapp = new Vue({
	  el: '#new-game',
	  data: {
	    teamNumber: {
	    	min: 2, 
	    	isError: false,
	    	value: 2
	    },
	    periodNumber:{
	    	min: 2, 
	    	isError: false
	    },
	    timeStart: {
	    	isError: false,
	    	isWork: false
	    },
	    timeDuration:{
	    	isError: false,
	    	isWork: false
	    },
	    cost: {
	    	isWork: true,
	    	default: 5,
	    	min: 3,
	    	max: 10,
		    isError: false
	    },
	    niokrSS: {
	    	isWork: true,
	    	default: 0,
	    	min: 0,
	    	max: 100,
		    isError: false
	    },
	    niokrQuality: {
	    	isWork: true,
	    	default: 0,
	    	min: 0,
	    	max: 100,
		    isError: false
	    },
	    NA: {
	    	isWork: true,
	    	volume: 0,
	    	factory: {
	    		isWork: true,
	    		isWorkSave: true,
	    		default: 0,
		    	min: 0,
		    	max: 999,
		    	isError: false
	    	},
	    	promotion: {
	    		isWork: true,
	    		isWorkSave: true,
	    		default: 0,
		    	min: 0,
		    	max: 100,
		    	isError: false
	    	}
	    	
	    },
	    Asia: {
	    	isWork: true,
	    	volume: 0,
	    	factory: {
	    		isWork: true,
	    		isWorkSave: true,
	    		default: 0,
		    	min: 0,
		    	max: 999,
		    	isError: false
	    	},
	    	promotion: {
	    		isWork: true,
	    		isWorkSave: true,
	    		default: 0,
		    	min: 0,
		    	max: 100,
		    	isError: false
	    	}
	    },
	    Europe: {
	    	isWork: true,
	    	volume: 0,
	    	factory: {
	    		isWork: true,
	    		isWorkSave: true,
	    		default: 0,
		    	min: 0,
		    	max: 999,
		    	isError: false
	    	},
	    	promotion: {
	    		isWork: true,
	    		isWorkSave: true,
	    		default: 0,
		    	min: 0,
		    	max: 100,
		    	isError: false
	    	}
	    },
	    basicParameters: {
	    	amountFactory: new Amount(1),
	    	amountOverheads: new Amount(5),
	    	amountDismantling: new Amount(3),
	    	startSS2: new Amount(1),
	    	startAttachmentsSS2: new Amount(3),
	    	startAttachmentsQuality2: new Amount(3),
	    	exponentSS2: new Amount(1),
	    	exponentQuality2: new Amount(1),
	    	baseFormulaCost2: new Amount(1)
	    },
	    averageVolume: 0,
	    isFormSubmit: true
	  },
	  methods: {
	  	updateError: function(obj, flag){
	  		obj.isError = flag;
	  		this.isFormSubmit = !flag;
	  	},
	  	validate: function(e, input){
	  		if(e.target.value < input.min)
	  			this.updateError(input, true);
	  		else 
	  			this.updateError(input, false);
	  		this.setAverageVolume();
	  	},
	  	updateAllVolumes: function(){
	  		this.updateAreaVolume(this.Asia);
	  		this.updateAreaVolume(this.Europe);
	  		this.updateAreaVolume(this.NA);
	  	},
	  	validAmount: function(obj){
	  		if(obj.val <= 0)
	  			this.updateError(obj, true);
	  		else
	  			this.updateError(obj, false);
	  	},
	  	validRange: function(obj){
	  		console.log('rr')
	  		if(+obj.min < +obj.max && 
	  			(+obj.default <= +obj.max && +obj.default >= +obj.min))
	  			this.updateError(obj, false);
	  		else
	  			this.updateError(obj, true);
	  	},
	  	updateAreaVolume: function(area){
	  		if (!this.teamNumber.isError && area.isWork){
	  			area.volume = getRandomVolume(this.teamNumber.value);
	  		} else {
	  			area.volume = 0;
	  		}
	  		this.setAverageVolume();
	  	},
	  	setAverageVolume: function(){
	  		if (!this.teamNumber.isError)
	  			this.averageVolume = (this.NA.volume + this.Asia.volume + this.Europe.volume) / this.teamNumber.value;
	  		else 
	  			this.averageVolume = 0;
	  	},
	  	changeAreaWork: function(area){
	  		if(area.isWork){
	  			area.factory.isWork = area.factory.isWorkSave;
	  			area.promotion.isWork = area.promotion.isWorkSave;
	  		} else {
	  			area.factory.isWorkSave = area.factory.isWork;
	  			area.factory.isWork = false;
	  			area.area.promotion.isWorkSave = area.promotion.isWork;
	  			area.promotion.isWork = false;
	  		}
	  	}
	  }
	})
});
