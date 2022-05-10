window.onload = isSignedIn;

function isSignedIn() {
    var url = 'checksignedin'

    fetch(url, {
        headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
        },
    })
    .then(response => {
        return response.json() //Convert response to JSON
    })
    .then(data => {
        //Perform actions with the response data from the view
        var is_Signed_In = data.response
        console.log(is_Signed_In) 
        
        if (is_Signed_In == 'true') {
            // getDetails();
            document.getElementById('SignUp-Here').style.display = 'none';
        }
        else {
            document.getElementById('Account-Menu').style.display = 'none';
        }     
    })    
}


//govind work do not touch


function getId(btn,str)
{
    var productId;
    var action;
    productId = btn.id;
    if(str == "view"){
        // window.location.href='./productdetail/{productID
        action="view";
        return 0;        
    }
    else if(str == "add"){
        action = "add";
    }
    else if(str == "remove"){
        action = "remove";
    }
    else if(str == "delete"){
        action = "delete";
    }
    console.log(productId,action);
    console.log('USER:', user)

    if (user == 'AnonymousUser'){
        // addCookieItem(productId, action)
        alert("not logged in")
    }else{
        updateUserOrder(productId, action)
    }
}

function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
            console.log('data:',data)
		});
}