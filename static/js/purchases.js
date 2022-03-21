const index_url = document.location.protocol + "//" + document.location.hostname + ":" + document.location.port + "/";

async function purchases(id_product) {
    let btn_purchases = document.getElementById("btn_purchases");
    let input_count_div = document.getElementById("input_count_purchases_div");
    let input_count = document.getElementById("input_count_purchases");
    let result = ''
    let method = ''
    let count = 0

    if (btn_purchases.hasAttribute('data-out')) {method = 'DELETE'} else {
        method = 'POST'
        count = input_count.value
    }

    if (method == 'POST') {
        result = await fetch(`${index_url}api/purchases/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
            },
            body: JSON.stringify({
                id_product: id_product,
                count: count
              })
        })
    } else {
        result = await fetch(`${index_url}api/purchases/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
            },
            body: JSON.stringify({
                id_product: id_product
              })
        })
    }
    const result_json = await result.json()
    console.log(result_json)

    if (result_json.success == 'true') {
        if (method == 'POST') {
            btn_purchases.classList.add('btn-outline-danger')
            btn_purchases.classList.remove('btn-outline-dark')
            btn_purchases.textContent = 'Удалить из корзины'
            btn_purchases.setAttribute('data-out', '')
            input_count_div.setAttribute('style', 'display: none')
        } else {
            btn_purchases.classList.add('btn-outline-dark')
            btn_purchases.classList.remove('btn-outline-danger')
            btn_purchases.textContent = 'Добавить в корзину'
            btn_purchases.removeAttribute('data-out')
            input_count_div.setAttribute('style', 'display: inline-block')
        }
    } else {
        alert(result_json.error)
    }
}