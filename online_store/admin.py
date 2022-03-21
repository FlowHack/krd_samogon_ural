from django.contrib import admin

from online_store.models import (Category, Characteristic, Product,
                                 QuantityCharacteristics, SubCategory, ProductImage, PreviewImage, Order, OrderItem)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    empty_value_display = '-пусто-'


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'title')
    search_fields = ('category', 'title')
    list_filter = ('category',)
    empty_value_display = '-пусто-'


@admin.register(Characteristic)
class CharacteristicAdmi(admin.ModelAdmin):
    list_display = ('title', 'dimension')
    search_fields = ('title',)
    empty_value_display = '-пусто-'


@admin.register(QuantityCharacteristics)
class QuantityCharacteristicsAdmin(admin.ModelAdmin):
    list_display = ('characteristic', 'quantity')
    search_fields = ('characteristic',)
    empty_value_display = '-пусто-'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'pub_date')
    list_filter = ('subcategory',)
    search_fields = ('title', 'price')
    empty_value_display = '-пусто-'


@admin.register(PreviewImage)
class PreviewImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'first')
    empty_value_display = '-пусто-'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product',)
    search_fields = ('product',)
    empty_value_display = '-пусто-'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_filter = ('state', 'date_state_in_processing', 'date_state_in_delivery', 'date_state_complete')
    empty_value_display = '-пусто-'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order_id')
    list_filter = ('order_id',)
    empty_value_display = '-пусто-'

    def order_id(self, obj):
        order_id = obj.order.id
        return order_id
