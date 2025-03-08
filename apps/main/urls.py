from django.urls import path
from .views import (
    Home,
    index,
)

app_name = 'hospital'

urlpatterns = [
    # **Region URLs**
    path('home', Home.as_view(), name='home'),
    path('', index, name='index'),
]
