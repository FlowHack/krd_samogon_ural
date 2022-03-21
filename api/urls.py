from django.urls import path
from api import views


app_name = 'api'

urlpatterns = [
    path('search_products/', views.search_product, name='search_products'),
    path('purchases/', views.purchases, name='purchases'),
    path('shopping-list/', views.shoppinglist, name='shopping-list'),
    path('change_count_product/', views.change_count_product, name='change_count_product'),
    path('make_order/', views.make_order, name='make_order'),
    path('to_order_call/', views.to_order_call, name='to_order_call'),
    path('get_subcategory_products/', views.get_subcategory_products, name='get_subcategory_products')
]
