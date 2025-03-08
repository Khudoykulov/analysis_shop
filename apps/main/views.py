from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.views.generic import TemplateView, CreateView
import csv
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
import csv
from django.conf import settings


def index(request):
    file_path = os.path.join(settings.BASE_DIR, 'data', 'product.csv')
    products = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                product = {
                    'name': row['name'],
                    'price': float(row['price']),
                    'store': row['store'],
                    'old_price': float(row.get('old_price', row['price'])) if row.get('old_price') else None,
                    'image': row.get('image', 'product01.png')
                }
                # Chegirma foizini hisoblash
                if product['old_price'] and product['price'] < product['old_price']:
                    discount = ((product['old_price'] - product['price']) / product['old_price']) * 100
                    product['discount'] = round(discount, 2)
                else:
                    product['discount'] = 0
                products.append(product)
    except FileNotFoundError:
        products = []
        print("Xato: products.csv fayli topilmadi!")

    query = request.GET.get('q', '')
    if query:
        products = [p for p in products if query.lower() in p['name'].lower()]

    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {
        'products': page_obj,
        'query': query,
        'page_obj': page_obj,
    })


# Create your views here.
class Home(TemplateView):
    template_name = 'index.html'
