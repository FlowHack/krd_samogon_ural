const index_url = document.location.protocol + "//" + document.location.hostname + ":" + document.location.port + "/";
let count = document.getElementById('section-shoplist').getAttribute('count')
let timeout = null;

function sleep(ms) {
  return new Promise(res => setTimeout(res, ms));
}

async function shopping_list(id_shopping_list) {
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
            id_shopping_list: id_shopping_list
          })
    })
    const result_json = await result.json()
    console.log(result_json)

    if (result_json.success == 'true') {
        let obj = document.getElementById("shopping-list-" + id_shopping_list)
        while (x < op) {op -= 0.01; obj.style.opacity = op; await sleep(5)}
        obj.remove()
        count -= 1
    }
    if (count == 0){
        document.location.href = index_url
    }
}