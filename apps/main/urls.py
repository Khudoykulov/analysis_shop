from django.urls import path
from .views import (
    Home,
    index,
    product_detail
)

app_name = 'main'

urlpatterns = [
    # **Region URLs**
    path('home/', Home.as_view(), name='home'),
    path('', index, name='index'),
    path('product/', product_detail, name='product_detail'),

]
