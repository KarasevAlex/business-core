$(document).ready(function(){
	var lastAsia = +$('.lastAsia').text();
	var lastEurope = +$('.lastEurope').text();
	var lastNA = +$('.lastNA').text();
	var allBudget = +$('.allBudget').text();
	var quality = +$('.quality').text();
	var ss = +$('.ss').text();

	var formapp = new Vue({
	  el: '#resolve-period',
	  data: {
	  	factories: {
	  		isError: false,
	  		isChange: false,
	  		Asia: {
	  			change: +AsiaFactory - +lastAsia,
	  			val: AsiaFactory,
	  			lastVal: lastAsia
	  		},
	  		Europe: {
	  			change: +EuropeFactory - +lastEurope,
	  			val: EuropeFactory,
	  			lastVal: lastEurope
	  		},
	  		NA: {
	  			change: +NAFactory - +lastNA,
	  			val: NAFactory,
	  			lastVal: lastNA
	  		}
	  	},
	  	niokrSS: niokrSS,
	  	niokrQuality: niokrQuality,
	  	promotion: {
	  		Asia: AsiaPromotion,
	  		NA: NAPromotion,
	  		Europe: EuropePromotion
	  	},
	  	spentBudgetVal: spentBudgetVal,
	  	allBudget: allBudget,
	  	SS: ss,
	  	quality: quality
	  },
	  methods: {
	  	changeFactory: function(factory){
	  		factory.change = +factory.val - +factory.lastVal;
	  		if(factory.change !== factory.change){
	  			factory.change = 0;
	  			this.factories.isError = true;
	  			return;	
	  		}
	  		var num = 0;
	  		for(i in this.factories)
	  			if(this.factories[i].change && this.factories[i].change != 0)
	  				num++;
	  		if(num === 0 || num === 1)
	  			this.factories.isError = false;
	  		else
	  			this.factories.isError = true;
	  		this.sizeBudget();

	  	},
	  	sizeBudget: function(){
	  		if(this.factories.isError)
	  			return;
	  		var Plant_Construction_Cost = 0;
	  		var Plant_Destruction_Cost = 0;

	  		for(i in this.factories)
	  			if(this.factories[i].change && this.factories[i].change != 0)
	  				if(this.factories[i].change > 0)
	  					Plant_Construction_Cost = 
	  						Math.ceil(this.factories[i].change * Plant_Construction);
	  				else
	  					Plant_Destruction_Cost = 
	  						Math.ceil(Math.abs(this.factories[i].change) * Plant_Destruction);
	  		var Plant_Overheads_Cost = Math.ceil(((+this.factories.NA.val) +
			(+this.factories.Asia.val) + (+this.factories.Europe.val)) * Plant_Overheads);
	  		var Prime_Cost = niokrSS;
	  		var Quality_Cost = niokrQuality;
	  		this.spentBudgetVal = Plant_Construction_Cost + Plant_Destruction_Cost + 
	  			Plant_Overheads_Cost + (+this.niokrSS) + (+this.niokrQuality) +
	  			(+this.promotion.NA) + (+this.promotion.Asia) + (+this.promotion.Europe);
	  		$('.budget').val(this.spentBudgetVal);
	  	},
	  	sizeSS: function(){
	  		var Prime_Cost_Acc_new = Prime_Cost_Acc + (+this.niokrSS);
	  		this.SS = Prime_Coststart + 1 - Math.pow((Prime_Cost_Acc_new / Prime_Costbase), (1 / Prime_Costcoef));
	  		this.SS = this.SS.toFixed(2);
	  		this.sizeBudget();
	  	},
	  	sizeQuality: function(){
	  	    var Quality_Cost_Acc_new = Quality_Cost_Acc + (+this.niokrQuality);
	  		this.quality = Math.pow((Quality_Cost_Acc_new / Quality_Costbase), (1 / Quality_Costcoef));
	  		this.quality = this.quality.toFixed(2);
	  		this.sizeBudget();
	  	}
	  }
	});

	//подсказки
	var help = $('.help-btn');
	help.each(function(i,e){
		var target = $(e);
		var content = target.next('.help-pane').html();
		target.webuiPopover({
			placement: 'bottom-right',
			width: 300,
			animation: 'pop',
			content: content,
			closeable: true,
			trigger:'click'
		});
	});
});