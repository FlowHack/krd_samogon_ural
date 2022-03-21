from django.urls import path

from online_store import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:id_category>/', views.category, name='category'),
    path('product/<int:id_product>', views.product, name='product'),
    path(
        'subcategory/<int:id_subcategory>', views.subcategory,
        name='subcategory'
    ),
    path('shoplist/', views.shop_list, name='shop_list'),
    path('orders/', views.orders, name='orders'),
    path('payment/', views.payment, name='payment')
]
