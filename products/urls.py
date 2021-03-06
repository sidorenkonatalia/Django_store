from django.urls import path

from products.views.views import products

app_name = 'products'

urlpatterns = [
    path('', products, name='index'),
    path('category/<int:category_id>', products, name='category'),
]