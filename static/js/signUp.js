$(function() {
    $('#btnSignUp').click(function() {
 
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                var signupObj = JSON.parse(response);
				var signup= document.getElementById("resul");
				var p= document.createElement("p");
				p.setAttribute("style","color:#E0FFFF");
				p.innerHTML = signupObj.result;
				signup.appendChild(p);
				setTimeout(function(){  
				window.location.reload();
				},850);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});