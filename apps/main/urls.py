from django.urls import path
from .views import (
    Home,
    Shops,
    Product,
    index,
    product_detail
)

app_name = 'main'

urlpatterns = [
    # **Region URLs**
    path('login/', Home.as_view(), name='home'),
    path('shops/', Shops.as_view(), name='shops'),
    path('product/', Product.as_view(), name='product'),
    path('', index, name='index'),
    path('product/<int:pk>/', product_detail, name='product_detail'),

]
