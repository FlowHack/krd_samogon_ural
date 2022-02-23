from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from online_store.models import PreviewImage, Category, Product, Order
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


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
def profile(request):
    return render(request, 'profile.html')


def subcategory(request, id_subcategory):
    pass


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
