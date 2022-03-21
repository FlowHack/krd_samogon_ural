const section = document.getElementById('main_section')
const index_url = document.location.protocol + "//" + document.location.hostname + ":" + document.location.port + "/";
const in_processing = Number(section.getAttribute('data-is-in_processing'))
const in_delivery = Number(section.getAttribute('data-is-in_delivery'))
const complete = Number(section.getAttribute('data-is-complete'))

if (in_processing == 0 & in_delivery == 0 & complete == 0){
    alert('У вас нет заказов! Вы будете перенаправлены на главную страницу!')
    document.location.href = index_url
}