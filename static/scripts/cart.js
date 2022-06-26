var updateButton = document.getElementsByClassName('update-cart')

for(var i=0;i<updateButton.length;i++){
    updateButton[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:',productId,'action:',action)
        console.log("USER:",user)
        if(user == 'AnonymousUser'){
            addCookieItem(productId,action)
        }
        else{
            updateUserOrder(productId,action)
        }
    })
}

function addCookieItem(productId,action){
    console.log("Not logged in")
    
    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity': 1}
        } 
        else{
            cart[productId]['quantity'] += 1
        }
    }
    if(action=='remove'){
       cart[productId]['quantity'] -= 1
       if(cart[productId]['quantity']<=0){
            console.log("removed Item")
            delete cart[productId]
       }
    }
    console.log("Cart:",cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

function updateUserOrder(productId,action){
    console.log("User is logged in sending data...")

    var url = '/update_item/'
    fetch(url,{
        method:'POST',
        headers:{
            'Context-Type':'spplication/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId':productId,'action':action})
    })

    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:',data)
        location.reload()
    })
}

if(user !='AnonymousUser'){
    document.getElementById('user-login').classList.add('hidden')
    document.getElementById('user-logout').classList.remove('hidden')
}

var logout_button = document.getElementById('user-logout')

logout_button.addEventListener('click',function(){
    document.getElementById('user-login').classList.remove('hidden')
    document.getElementById('user-logout').classList.add('hidden')
})