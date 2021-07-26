$(document).ready(function(){
	// Product Filter Start
	// # = id
	$("#priceFilterBtn").on('click',function(){
		var _filterObj={};
		var _minPrice=$('#maxPrice').attr('min');
		var _maxPrice=$('#maxPrice').val();
		_filterObj.minPrice=_minPrice;
		_filterObj.maxPrice=_maxPrice;

		// Run Ajax
		$.ajax({
			url:'/ajax_filter_price',
			data:_filterObj,
			dataType:'json',
			success:function(res){
				console.log(res);
				$("#filteredProducts").html(res.data);
			}
		});
	});
	// End

	// Filter Product According to the price
	$("#maxPrice").on('blur',function(){
		var _min=$(this).attr('min');
		var _max=$(this).attr('max');
		var _value=$(this).val();
		console.log(_value,_min,_max);
		if(_value < parseInt(_min) || _value > parseInt(_max)){
			alert('Values should be '+_min+'-'+_max);
			$(this).val(_min);
			$(this).focus();
			$("#rangeInput").val(_min);
			return false;
		}
	});
	// End
});