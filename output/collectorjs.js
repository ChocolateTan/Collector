    function onClickAction(month, id){
        var eObject = document.getElementById('div_'+id);
        var aObject = document.getElementById('a_'+id);
        
        if(eObject.style.display == 'none'){
            eObject.style.display = '';
            aObject.innerHTML = '[收起]';
        }else{
            eObject.style.display = 'none';
            aObject.innerHTML = '[展开]';
        }
        checkClose(month, id);
    }

    function checkClose(month, id){
        let storage = window.localStorage;
        let key = 'month_' + month;
        cart = storage.getItem(key);
        if (!cart) {
            cart.push(id);
            window.localStorage.setItem(key, JSON.stringify(cart));
        } else {
            cart = JSON.parse(window.localStorage.getItem(key));
            if (cart.indexOf(id) > -1) {
                cart.remove(id);
            } else {
                cart.push(id);
            }
            window.localStorage.setItem(key, JSON.stringify(cart));
        }
    }