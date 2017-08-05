$(function(){
		$.ajax({
			url : '/getAllWords',
			type : 'GET',
			success: function(res){
				var div1 = $('<div>')
				.attr('class', 'comment-author vcard')
				.append($('<b>')
					.attr('class','fn'),
							$('<span>')
							.attr('class', 'says'));
				var div2 = $('<div>')
				.attr('class', 'comment-metadata')
				.append($('<time>')
					.attr('datetime','2017-05-05T18:56:06+00:00'));
				var div3 = $('<div>')
					.attr('class','fn')
					.append($('<p>'));	
				var wordsObj = JSON.parse(res);
				var words1= '';
				var words2= '';
				var words3= '';
				$.each(wordsObj,function(index, value){
					words1= $(div1).clone();
					words2= $(div2).clone();
					words3= $(div3).clone();
					$(words1).find('b').text(value.Id);
					$(words1).find('span').text("说:");
					$(words2).find('time').text(value.Time);
					$(words3).find('p').text(value.Description);
					$('.comment-area').append(words1).append(words2).append(words3);
				});
			},
			error: function(error){
				console.log(error);
			}
		});
	});