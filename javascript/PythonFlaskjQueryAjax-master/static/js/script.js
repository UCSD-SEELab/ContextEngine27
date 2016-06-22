$(function(){
	$('button').click(function(){
		var num = $('#accessorNum').val();
		//create an array or list
		
		var a = initialize();
		a.provideInput('input', num);
		var a = initialize();
		var react = a.react();
		var outputFromAccessor = a.latestOutput('output');

		// return outputFromAccessor;





		$.ajax({
			url: '/accessorOutput',
			data: outputFromAccessor,
			type: 'POST',
			success: function(response){
				console.log("success");
			},
			error: function(error){
				console.log("error");
			}
		});
	});
});
