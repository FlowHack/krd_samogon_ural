let timeout = null;
let blur_timeout = null;
const index_url = document.location.protocol + "//" + document.location.hostname + ":" + document.location.port + "/";
const input_search = document.getElementById("search");
const hint = document.getElementById("hint_search");

input_search.addEventListener("blur", async function () {
  clearTimeout(blur_timeout);
  blur_timeout = setTimeout(async function () {
    hint.style.display = "none";
    hint.innerHTML = "";
  }, 300)
});

async function showHint(request) {
  clearTimeout(timeout);
  timeout = setTimeout(async function () {
    hint.innerHTML = "";
    request = request.trim();

    if (request.length != 0) {
      const result = await fetch(`${index_url}api/search_products/?query=${request}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        }
      });
      const products = await result.json();

      if (products.length == 0) {
        hint.style.display = "none";
      } else {
        hint.style.display = "block";
      }
      for (let i = 0; i <= products.length - 1; i++) {
        product = products[i];
        let product_hint = document.createElement("a");
        product_hint.className = "url_product";
        product_hint.innerHTML = product.title;
        product_hint.href = new URL(index_url + "product/" + product.id);
        hint.appendChild(product_hint);
      }
    } else {
      hint.style.display = "none";
    }
  }, 500);
}
