from django.shortcuts import render
from django.shortcuts import get_object_or_404
from online_store.models import PreviewImage, Category, Product, Order, SubCategory
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Min


User = get_user_model()


def index(request):
    image_objects = PreviewImage.objects.all()
    context = {
        'images': image_objects,
        'is_first': image_objects.filter(first=True).exists(),
        'categories': Category.objects.all()
    }
    return render(request, 'index.html', context=context)


def category(request, id_category):
    category = get_object_or_404(Category, id=id_category)
    subcategories = category.in_subcategories.all()

    context = {
        'category': category,
        'subcategories': subcategories
    }
    return render(request, 'category.html', context=context)


def product(request, id_product):
    product = get_object_or_404(Product, id=id_product)
    images = product.images.all()
    equipments = product.equipment.split('&&')

    context = {
        'product': product,
        'images': images,
        'is_first': images.filter(first=True).exists(),
        'equipments': equipments
    }
    return render(request, 'product.html', context=context)


@login_required
def orders(request):
    orders_user = Order.objects.filter(user=request.user).exclude(state=Order.StatusOrder.SHOPPINGLIST)
    in_processing = orders_user.filter(state=Order.StatusOrder.INPROCESSING)
    in_delivery = orders_user.filter(state=Order.StatusOrder.INDELIVERY)
    complete = orders_user.filter(state=Order.StatusOrder.ORDERCOMPLETE)

    context = {
        'in_processing': in_processing,
        'in_delivery': in_delivery,
        'complete': complete,
    }
    return render(request, 'orders.html', context=context)


def subcategory(request, id_subcategory):
    _subcategory = get_object_or_404(SubCategory, id=id_subcategory)
    products = _subcategory.in_products.all().order_by('-pub_date')
    max_min_price = products.aggregate(Max('price'), Min('price'))
    min_price = round(max_min_price.get('price__min'))
    max_price = round(max_min_price.get('price__max'))
    start_min_price = min_price
    start_max_price = max_price

    context = {
        'subcategory': _subcategory,
        'products': products,
        'min_price': min_price,
        'max_price': max_price,
        'start_min_price': start_min_price,
        'start_max_price': start_max_price
    }
    return render(request, 'subcategory.html', context=context)


@login_required
def shop_list(request):
    order, result = request.user.in_orders.get_or_create(
        user=request.user, state=Order.StatusOrder.SHOPPINGLIST
    )
    items = order.items.all()
    count = int(items.count())
    sum_price = order.get_total_cost()

    context = {
        'shopping_list': items,
        'sum_price': sum_price,
        'count': count
    }

    return render(request, 'shop_list.html', context=context)


def payment(request):
    context = {
        'title': 'Оплата',
        'title_h': 'Оплата',
        'message': 'После заказа товара с вами свяжется наш менеджер.'
    }
    return render(request, 'customPage.html', context=context)


def delivery(request):
    context = {}
    return render()
