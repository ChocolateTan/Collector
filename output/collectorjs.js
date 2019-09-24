    function onClickAction(month, id){
        var eObject = document.getElementById('div_'+id);
        var aObject = document.getElementById('a_'+id);
        
        if(eObject.style.display == 'none'){
            eObject.style.display = '';
            aObject.innerHTML = '[展开]';
        }else{
            eObject.style.display = 'none';
            aObject.innerHTML = '[收起]';
            eObject.innerHTML = eObject.getAttribute('data-desc');
        }
        checkClose(month, id);
    }

    function checkClose(month, id){
        let storage = window.localStorage;
        let key = 'month_' + month;
        cart = storage.getItem(key);

        if(!cart){
            cart = [];
            cart.push(id);
            storage.setItem(key, JSON.stringify(cart));
        }else{
            cart = JSON.parse(storage.getItem(key));
            var index = cart.indexOf(id);
            if (index > -1) {
                cart.splice(index, 1);
                storage.setItem(key, JSON.stringify(cart));
            } else {
                cart.push(id);
                storage.setItem(key, JSON.stringify(cart));
            }
        }
    }