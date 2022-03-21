const rangeSliderInit = () => {
    const range = document.getElementById('range');
    const min_value_start = Number(range.getAttribute('data-start-min-value'))
    const max_value_start = Number(range.getAttribute('data-start-max-value'))
    const min_value = Number(range.getAttribute('data-min-value'))
    const max_value = Number(range.getAttribute('data-max-value'))

    if (!range) return

    noUiSlider.create(range, {
        animation: true,
        start: [min_value_start, max_value_start],
        connect: true,
        range: {'min': min_value, 'max': max_value},
        tooltips: true,
        format: wNumb({decimals: 0, thousand: '.', postfix: ' ₽'}),
        step: 1,
    })
}

const init = () => {rangeSliderInit()}
window.addEventListener('DOMContentLoaded', init)

function click_radio_data(element) {
    if (element.hasAttribute('checked')) {
        element.removeAttribute('checked')
        element.id = 'flexSwitchCheckDefault'
    } else {
        element.setAttribute('checked', '')
        element.id = 'flexSwitchCheckChecked'
    }
}

async function apply_filters(id_subcategory) {
    let download = document.getElementById('download-div')
    download.setAttribute('style', 'display: block;')
    let element = document.getElementsByClassName('noUi-handle noUi-handle-lower')[0]
    let min_value = Number(element.getAttribute('aria-valuenow'))
    let max_value = Number(element.getAttribute('aria-valuemax'))
    let checked_element = ''

    if (document.getElementById('flexSwitchCheckChecked')) {checked_element = document.getElementById('flexSwitchCheckChecked')}
    else {checked_element = document.getElementById('flexSwitchCheckDefault')}
    checked = checked_element.hasAttribute('checked')

    const result = await fetch(`${index_url}api/get_subcategory_products/?id_subcategory=${id_subcategory}&filter_date=${checked}&min_price=${min_value}&max_price=${max_value}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    });
    const result_json = await result.json()

    if (result_json.success == 'true') {
        const index_url = document.location.protocol + "//" + document.location.hostname + ":" + document.location.port + "/";
        let div = document.getElementById('wrapper_cards')
        div.innerHTML = ''
        let products = result_json.message.products
        let media_url = result_json.message.media_url
        let static_url = result_json.message.static_url

        for (let i = 0; i <= products.length - 1; i++) {
            product = products[i]
            let id = String(product.id)
            let preview_img = product.preview_image
            let title = product.title
            let price = product.price

            let col_div = document.createElement('div')
            col_div.className = 'col'

            let card_content = document.createElement('div')
            col_div.appendChild(card_content)
            card_content.className = 'card-content card h-100 border-secondary'

            let card_a_img = document.createElement('a')
            card_content.appendChild(card_a_img)
            card_a_img.href = new URL(index_url + 'product/' + id)
            let img = document.createElement('img')
            card_a_img.appendChild(img)
            img.className = 'card-img card-img-top'
            if (preview_img) img.setAttribute('src', `${media_url}${preview_img}`)
            else img.setAttribute('src', `${static_url}${preview_img}`)

            let title_div = document.createElement('div')
            card_content.appendChild(title_div)
            title_div.className = 'card-body'
            title_div.setAttribute('style', 'padding: 0')
            let title_h = document.createElement('h5')
            title_div.appendChild(title_h)
            title_h.className = 'title_card card-title'
            title_h.setAttribute('align', 'center')
            title_h.innerHTML = title

            let ul_price = document.createElement('ul')
            card_content.appendChild(ul_price)
            ul_price.className = 'list-group list-group-flush'
            let li_price = document.createElement('li')
            ul_price.appendChild(li_price)
            li_price.setAttribute('align', 'center')
            li_price.className = 'characteristic-li list-group-item'
            li_price.innerHTML = `₽ ${price}`

            let hr_price =  document.createElement('hr')
            card_content.appendChild(hr_price)
            hr_price.setAttribute('style', 'margin: 0')

            let card_body = document.createElement('div')
            card_content.appendChild(card_body)
            card_body.className = 'card-body'
            let a_body = document.createElement('a')
            card_body.appendChild(a_body)
            a_body.href = new URL(index_url + 'product/' + id)
            a_body.className = 'btn_card btn-center btn btn-outline-dark'
            a_body.setAttribute('type', 'button')
            a_body.innerHTML = 'Перейти'

            div.appendChild(col_div)
        }
        download.removeAttribute('style')
    } else {
        alert(result_json.error)
        download.removeAttribute('style')
    }
}
