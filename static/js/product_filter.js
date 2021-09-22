$(document).ready(function(){  // quando il documento è pronto chiama questa funzione
	// Product filter start
	// # = id
	$("#priceFilterBtn").on('click',function(){ // al clic del bottone Apply lancia questa funzione
		var _filterObj={};
		var _minPrice=$('#maxPrice').attr('min'); // viene preso l'attributo minimo
		var _maxPrice=$('#maxPrice').val(); // viene preso il valore corrente
		// aggiunge al dizionario questi valori
		_filterObj.minPrice=_minPrice;
		_filterObj.maxPrice=_maxPrice;

		// Run Ajax
		$.ajax({
			url:'/ajax_filter_price',
			data:_filterObj, // gli passo il json (tipo dizionario)
			dataType:'json',
			// ritorna un oggetto Json da filter_price (views.py) contentente filtered_products_price.html in
			// formato stringa.
			success:function(res){
				console.log(res);
				// va a chiamare l'id con nome filteredProducts e incapsula l'html preso in precedenza (filtered_products_price.html)
				$("#filteredProducts").html(res.data);
			}
		});
	});

	// Filter Product According to the price. Entra in questa funzione quando clicco fuori dalla casella di testo.
	$("#maxPrice").on('blur',function(){
		var _min=$(this).attr('min'); // variabile che prende il valore minimo dalla casella di testo
		var _max=$(this).attr('max');
		var _value=$(this).val(); // valore dentro la casella
		// console.log(_value,_min,_max);
		if(_value < parseInt(_min) || _value > parseInt(_max)){
			alert('Values should be '+_min+'-'+_max);
			$(this).val(_min); // _min viene risettato al valore minimo
			$(this).focus(); // la casella di testo viene ricliccata
			$("#rangeInput").val(_min); // lo scroll viene ritornato al valore minimo
			return false;
		}
	});
});