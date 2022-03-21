let count = document.getElementById('section-shoplist').getAttribute('count')

if (count == 0){
    alert('У вас нет товаров в корзине! Вы будете перенаправлены на главную страницу!')
    document.location.href = index_url
}

function sleep(ms) {
  return new Promise(res => setTimeout(res, ms));
}

async function shopping_list(id_order_item) {
    let result = ''
    let x = 0.1
    let op = 1.0

    result = await fetch(`${index_url}api/shopping-list/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        body: JSON.stringify({
            id_order_item: id_order_item
          })
    })
    const result_json = await result.json()
    console.log(result_json)

    if (result_json.success == 'true') {
        let obj = document.getElementById("shopping-list-" + id_order_item)
        while (x < op) {op -= 0.01; obj.style.opacity = op; await sleep(5)}
        obj.remove()
        count -= 1
    } else {
        alert(result.error)
    }
    if (count == 0){
        document.location.href = index_url
    }
}

async function change_count_product(id_order_item, operand) {
    let input = document.getElementById('input_count_purchases-' + id_order_item)
    let value = Number(input.getAttribute('value'))

    if (operand == '+') {
        value += 1
        input.removeAttribute('value')
        input.setAttribute('value', value)
    } else {
        value -= 1
        input.removeAttribute('value')
        input.setAttribute('value', value)
    }

    count_product(id_order_item, value)
}

async function count_product(id_order_item, value) {
    let price_product = document.getElementById('price-order-item-' + id_order_item)
    let total_price = document.getElementById('total-price')

    result = await fetch(`${index_url}api/change_count_product/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        body: JSON.stringify({
            id_order_item: id_order_item,
            value: value
          })
    })
    const result_json = await result.json()
    console.log(result_json)

    if (result_json.result == 'true') {
        price_product.textContent = `Цена: ${result_json.price}руб.`
        total_price.textContent = `Итого: ${result_json.total_price}руб.`
    } else {
        alert(result_json.error)
    }
}

async function order(url) {
    result = await fetch(`${index_url}api/make_order/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
        }
    })
    const result_json = await result.json()

    if (result_json.success == 'true') {
        alert('Удачно! Вы будете перенаправлены на страницу заказов.')
        document.location.href = url
    } else {
        alert('Попробуйте позже.')
        alert(result_json)
    }
}