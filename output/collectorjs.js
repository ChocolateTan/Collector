    function onClickAction(id){
        var eObject = document.getElementById('div_'+id);
        var aObject = document.getElementById('a_'+id);
        
        if(eObject.style.display == 'none'){
            eObject.style.display = '';
            aObject.innerHTML = '[收起]';
        }else{
            eObject.style.display = 'none';
            aObject.innerHTML = '[展开]';
        }
    }

    function checkClose(month, id){
        let storage = window.localStorage;
        if (!storage.getItem('month_' + month)) {
            cart.push(id);
            window.localStorage.setItem("cartLocal", JSON.stringify(cart));
        } else {
            cart = JSON.parse(window.localStorage.getItem('month_' + month));
            if (cart.indexOf(id) > -1) {
                cart.remove(id);
            } else {
                cart.push(id);
            }
            window.localStorage.setItem("cartLocal", JSON.stringify(cart));
        }
    }