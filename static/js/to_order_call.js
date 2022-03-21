async function to_order_call(id_element) {
    let result = ''
    let element = document.getElementById(id_element)
    let need_replace = element.getAttribute('need_replace')
    let what_replace_id = element.getAttribute('what_replace_id')
    let on_what_replace_id = ''
    let on_what_replace = ''

    if (need_replace == 'true') {
        on_what_replace_id = element.getAttribute('on_what_replace_id')
        on_what_replace = document.getElementById(on_what_replace_id)
        if (what_replace_id) {element = document.getElementById(what_replace_id)}

        element.setAttribute('style', 'display: None')
        on_what_replace.setAttribute('style', 'display: block')
    }

    result = await fetch(`${index_url}api/to_order_call/`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        }
     })
    const result_json = await result.json()
    console.log(result_json)

    if (result_json.success == 'true') {
        alert(result_json.message)
    } else {
        alert(result_json.error)
    }

    if (need_replace == 'true') {
        element.removeAttribute('style')
        on_what_replace.removeAttribute('style')
    }
}