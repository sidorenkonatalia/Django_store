from django.contrib import admin

from products.models import ProductCategory, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quality', 'category')
    fields = ('name', 'image', 'description', ('price', 'quality', 'category'))
    search_fields = ('name', 'category__name')
    ordering = ('category__name',)


admin.site.register(ProductCategory)

# Register your models here.
